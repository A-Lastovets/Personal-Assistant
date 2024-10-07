from django.urls import path
from .views import ExchangeRateAndNewsView

urlpatterns = [
    path('home/', ExchangeRateAndNewsView.as_view(), name='news_summary')
]
