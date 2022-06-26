from django.urls import path
from .views import TramStopAPIView, ApiView

urlpatterns = [
    path('', ApiView.as_view()),
    path('stops/', TramStopAPIView.as_view()),
]
