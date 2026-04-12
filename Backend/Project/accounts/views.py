from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import RegistrationSerializer, EntrepreneurProfileSerializer, InvestorProfileSerializer, UserSerializer
from .models import EntrepreneurProfile, InvestorProfile

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegistrationSerializer

class UserProfileView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        if user.role == 'entrepreneur':
            try:
                profile = user.entrepreneur_profile
                serializer = EntrepreneurProfileSerializer(profile)
                return Response(serializer.data)
            except EntrepreneurProfile.DoesNotExist:
                return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
        elif user.role == 'investor':
            try:
                profile = user.investor_profile
                serializer = InvestorProfileSerializer(profile)
                return Response(serializer.data)
            except InvestorProfile.DoesNotExist:
                return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = UserSerializer(user)
            return Response(serializer.data)

class EntrepreneurProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = EntrepreneurProfile.objects.all()
    serializer_class = EntrepreneurProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user.entrepreneur_profile

class InvestorProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = InvestorProfile.objects.all()
    serializer_class = InvestorProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user.investor_profile
