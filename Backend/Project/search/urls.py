from django.urls import path
from .views import StartupSearchView, InvestorSearchView

urlpatterns = [
    path('startups/', StartupSearchView.as_view(), name='search-startups'),
    path('investors/', InvestorSearchView.as_view(), name='search-investors'),
]
