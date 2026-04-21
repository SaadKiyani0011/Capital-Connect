from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Meeting(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
    inviter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meetings_created')
    invitee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meetings_received')
    topic = models.CharField(max_length=255)
    scheduled_at = models.DateTimeField()
    duration_minutes = models.IntegerField(default=30)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.topic} between {self.inviter.username} and {self.invitee.username} at {self.scheduled_at}"
