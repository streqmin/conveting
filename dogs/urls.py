from django.urls import path
from .views import DogPublicDetailView, DogCreateView, DogUpdateView

urlpatterns = [
    path("add/", DogCreateView.as_view(), name="dog_add"),
    path("<uuid:pk>/", DogPublicDetailView.as_view(), name="dog_detail"),
    path("<uuid:pk>/edit/", DogUpdateView.as_view(), name="dog_edit"),
]
