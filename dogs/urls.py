from django.urls import path
from .views import DogPublicDetailView, DogCreateView, DogUpdateView

urlpatterns = [
    path("dog/add/", DogCreateView.as_view(), name="dog_add"),
    path("dog/<uuid:dog_id>/", DogPublicDetailView.as_view(), name="dog_detail"),
    path("dog/<uuid:dog_id>/edit/", DogUpdateView.as_view(), name="dog_edit"),
]
