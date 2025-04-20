from django.urls import path
from .views import PredictionCreateView

urlpatterns = [
    path("create/", PredictionCreateView.as_view(), name="prediction_create"),
]
