from django.urls import path
from .views import ExchangeRateNewsView

urlpatterns = [
    path('home/', ExchangeRateNewsView.as_view(), name='exchange_rate_news'),
]
