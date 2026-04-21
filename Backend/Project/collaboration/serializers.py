from rest_framework import serializers
from .models import Meeting
import datetime
from django.db.models import Q

class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = '__all__'
        read_only_fields = ('inviter', 'status', 'created_at', 'updated_at')

    def validate(self, data):
        scheduled_at = data.get('scheduled_at')
        duration = data.get('duration_minutes', 30)
        invitee = data.get('invitee')
        
        request = self.context.get('request')
        if not request or not hasattr(request, 'user'):
            return data
            
        inviter = request.user
        
        if scheduled_at and invitee:
            # We assume a Meeting overlaps if it starts within `duration` + 10 mins buffer
            # A more precise query: any existing meeting where existing_start < new_end AND existing_end > new_start
            # But since we only have scheduled_at and duration, we will do a simpler check.
            
            end_time = scheduled_at + datetime.timedelta(minutes=duration)
            
            # We fetch all accepted meetings for either user and check in python to be safe with durations
            invitee_meetings = Meeting.objects.filter(
                Q(inviter=invitee) | Q(invitee=invitee),
                status='accepted',
                scheduled_at__date=scheduled_at.date() # Narrow down to the same day
            )
            for m in invitee_meetings:
                m_end = m.scheduled_at + datetime.timedelta(minutes=m.duration_minutes)
                if m.scheduled_at < end_time and m_end > scheduled_at:
                    raise serializers.ValidationError("The invitee is already booked during this time.")

            inviter_meetings = Meeting.objects.filter(
                Q(inviter=inviter) | Q(invitee=inviter),
                status='accepted',
                scheduled_at__date=scheduled_at.date()
            )
            for m in inviter_meetings:
                m_end = m.scheduled_at + datetime.timedelta(minutes=m.duration_minutes)
                if m.scheduled_at < end_time and m_end > scheduled_at:
                    raise serializers.ValidationError("You are already booked during this time.")

        return data
        
    def create(self, validated_data):
        validated_data['inviter'] = self.context['request'].user
        return super().create(validated_data)
