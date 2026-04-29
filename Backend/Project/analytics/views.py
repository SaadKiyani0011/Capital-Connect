from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from collaboration.models import Meeting
from documents.models import Document

class DashboardAnalyticsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        
        # Calculate meeting stats
        total_meetings = Meeting.objects.filter(Q(inviter=user) | Q(invitee=user)).count()
        pending_meetings = Meeting.objects.filter(Q(inviter=user) | Q(invitee=user), status='pending').count()
        upcoming_meetings = Meeting.objects.filter(Q(inviter=user) | Q(invitee=user), status='accepted').count()
        
        # Calculate document stats
        total_documents = Document.objects.filter(Q(owner=user) | Q(is_shared=True)).count()
        signed_documents = Document.objects.filter(Q(owner=user) | Q(is_shared=True), status='signed').count()
        
        return Response({
            "meetings": {
                "total": total_meetings,
                "pending": pending_meetings,
                "upcoming": upcoming_meetings
            },
            "documents": {
                "total": total_documents,
                "signed": signed_documents
            }
        })
