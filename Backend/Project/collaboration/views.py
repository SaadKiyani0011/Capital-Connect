from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from .models import Meeting
from .serializers import MeetingSerializer

class MeetingListCreateView(generics.ListCreateAPIView):
    serializer_class = MeetingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Meeting.objects.filter(Q(inviter=user) | Q(invitee=user)).order_by('-scheduled_at')

class MeetingDetailView(generics.RetrieveAPIView):
    serializer_class = MeetingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Meeting.objects.filter(Q(inviter=user) | Q(invitee=user))

class MeetingStatusUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        try:
            meeting = Meeting.objects.get(pk=pk)
        except Meeting.DoesNotExist:
            return Response({"error": "Meeting not found."}, status=status.HTTP_404_NOT_FOUND)

        # Only the invitee can accept or reject the meeting
        if request.user != meeting.invitee:
            return Response({"error": "You do not have permission to change this meeting's status."}, status=status.HTTP_403_FORBIDDEN)

        new_status = request.data.get('status')
        if new_status not in ['accepted', 'rejected']:
            return Response({"error": "Invalid status. Must be 'accepted' or 'rejected'."}, status=status.HTTP_400_BAD_REQUEST)

        # Before accepting, ensure there's no overlap again just in case another meeting was accepted meanwhile
        if new_status == 'accepted':
            # Run the overlap check
            serializer = MeetingSerializer(meeting, data={'status': 'accepted'}, partial=True, context={'request': request})
            # To trigger validation with existing data, we pass scheduled_at and duration_minutes and invitee fake
            # Wait, our serializer validate logic triggers on scheduled_at presence.
            # Let's do a direct ORM check for safety
            import datetime
            end_time = meeting.scheduled_at + datetime.timedelta(minutes=meeting.duration_minutes)
            user = request.user
            
            conflicts = Meeting.objects.filter(
                Q(inviter=user) | Q(invitee=user),
                status='accepted',
                scheduled_at__date=meeting.scheduled_at.date()
            ).exclude(pk=meeting.pk)
            
            for m in conflicts:
                m_end = m.scheduled_at + datetime.timedelta(minutes=m.duration_minutes)
                if m.scheduled_at < end_time and m_end > meeting.scheduled_at:
                    return Response({"error": "You already have an accepted meeting during this time."}, status=status.HTTP_400_BAD_REQUEST)

        meeting.status = new_status
        meeting.save()
        return Response({"status": f"Meeting {new_status}."})
