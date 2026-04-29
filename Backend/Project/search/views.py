from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from accounts.models import EntrepreneurProfile, InvestorProfile
from accounts.serializers import EntrepreneurProfileSerializer, InvestorProfileSerializer

class StartupSearchView(generics.ListAPIView):
    queryset = EntrepreneurProfile.objects.all()
    serializer_class = EntrepreneurProfileSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Exact or partial match filters
    filterset_fields = {
        'industry': ['exact', 'icontains'],
        'location': ['exact', 'icontains'],
        'foundedYear': ['gte', 'lte', 'exact'],
    }
    
    # Text search
    search_fields = ['startupName', 'pitchSummary', 'industry', 'location']
    
    # Ordering
    ordering_fields = ['foundedYear', 'teamSize']

class InvestorSearchView(generics.ListAPIView):
    queryset = InvestorProfile.objects.all()
    serializer_class = InvestorProfileSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    filterset_fields = {
        'totalInvestments': ['gte', 'lte'],
    }
    
    # Text search over related user or JSON fields natively in postgres/sqlite might differ,
    # but basic text search usually handles text fields well. 
    # For JSONFields, we might need custom logic, but for now we search username and bio
    search_fields = ['user__username', 'user__bio', 'minimumInvestment', 'maximumInvestment']
    
    ordering_fields = ['totalInvestments']
