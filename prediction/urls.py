from django.urls import path
from .views import PredictionCreateView, PredictionResultView

urlpatterns = [
    path("create/", PredictionCreateView.as_view(), name="prediction_create"),
    path("results/<uuid:request_id>/", PredictionResultView.as_view(), name="prediction_result"),
]
