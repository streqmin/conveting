from django.urls import path
from .views import NearestHospitalsView

urlpatterns = [
    path("nearest/", NearestHospitalsView.as_view(), name="nearest_hospitals"),
]
