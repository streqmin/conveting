from django.urls import path
from .views import PostCreateView, PostListView, PostDetailView, toggle_like, CommentCreateView

urlpatterns = [
    path("", PostListView.as_view(), name="post_list"),
    path("<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("<int:post_id>/toggle-like/", toggle_like, name="toggle_like"),
    path("<int:post_id>/comment/", CommentCreateView.as_view(), name="comment_create"),
    path("create/", PostCreateView.as_view(), name="post_create"),
]
