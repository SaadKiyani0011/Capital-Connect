from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import EntrepreneurProfile, InvestorProfile

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'avatarUrl', 'bio', 'isOnline', 'date_joined')
        read_only_fields = ('id', 'date_joined')

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'role')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            role=validated_data.get('role', 'entrepreneur')
        )
        
        # Create corresponding profile
        if user.role == 'entrepreneur':
            EntrepreneurProfile.objects.create(user=user)
        elif user.role == 'investor':
            InvestorProfile.objects.create(user=user)
            
        return user

class EntrepreneurProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = EntrepreneurProfile
        fields = '__all__'

class InvestorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = InvestorProfile
        fields = '__all__'
