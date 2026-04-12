from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('entrepreneur', 'Entrepreneur'),
        ('investor', 'Investor'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='entrepreneur')
    avatarUrl = models.URLField(max_length=500, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    isOnline = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.email} ({self.role})"

class EntrepreneurProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='entrepreneur_profile')
    startupName = models.CharField(max_length=255, blank=True, null=True)
    pitchSummary = models.TextField(blank=True, null=True)
    fundingNeeded = models.CharField(max_length=100, blank=True, null=True)
    industry = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    foundedYear = models.IntegerField(blank=True, null=True)
    teamSize = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.startupName} ({self.user.username})"

class InvestorProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='investor_profile')
    investmentInterests = models.JSONField(blank=True, null=True, default=list) # List of strings e.g., ["Tech", "Health"]
    investmentStage = models.JSONField(blank=True, null=True, default=list) # e.g., ["Seed", "Series A"]
    portfolioCompanies = models.JSONField(blank=True, null=True, default=list)
    totalInvestments = models.IntegerField(default=0)
    minimumInvestment = models.CharField(max_length=100, blank=True, null=True)
    maximumInvestment = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - Investor"
