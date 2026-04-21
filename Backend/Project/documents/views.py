from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Q
from .models import Document
from .serializers import DocumentSerializer

class DocumentListCreateView(generics.ListCreateAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        user = self.request.user
        return Document.objects.filter(Q(owner=user) | Q(is_shared=True)).order_by('-uploaded_at')

class DocumentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        user = self.request.user
        return Document.objects.filter(Q(owner=user) | Q(is_shared=True))
