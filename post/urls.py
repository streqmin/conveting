from django.urls import path
from .views import (
    PostCreateView,
    PostListView,
    PostDetailView,
    CommentCreateView,
    PostLikeToggleView,
    CommentLikeToggleView,
)

urlpatterns = [
    path("", PostListView.as_view(), name="post_list"),
    path("create/", PostCreateView.as_view(), name="post_create"),
    path("<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("<int:post_id>/comment/", CommentCreateView.as_view(), name="comment_create"),
    path("<int:post_id>/like/", PostLikeToggleView.as_view(), name="post_like_toggle"),
    path(
        "comment/<int:comment_id>/like/",
        CommentLikeToggleView.as_view(),
        name="comment_like_toggle",
    ),
]
