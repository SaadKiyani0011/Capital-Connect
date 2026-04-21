from django.urls import path
from .views import MeetingListCreateView, MeetingDetailView, MeetingStatusUpdateView

urlpatterns = [
    path('meetings/', MeetingListCreateView.as_view(), name='meeting-list-create'),
    path('meetings/<int:pk>/', MeetingDetailView.as_view(), name='meeting-detail'),
    path('meetings/<int:pk>/status/', MeetingStatusUpdateView.as_view(), name='meeting-status-update'),
]
