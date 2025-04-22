from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView


from .models import Post, PostLike, Comment
from .forms import PostForm, CommentForm


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "post/post_form.html"
    success_url = reverse_lazy("post_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PostListView(ListView):
    model = Post
    template_name = "post/post_list.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.select_related("user", "dog", "disease").order_by("-created_at")

        # 검색어
        search_query = self.request.GET.get("q")
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | Q(content__icontains=search_query)
            )

        # 작성자 ID 필터
        user_id = self.request.GET.get("user")
        if user_id:
            queryset = queryset.filter(user__id=user_id)

        # 견종 필터
        breed = self.request.GET.get("breed")
        if breed:
            queryset = queryset.filter(breed=breed)

        # 질환 ID 필터
        disease_id = self.request.GET.get("disease")
        if disease_id:
            queryset = queryset.filter(disease__id=disease_id)

        # 질환 부위 필터 (예: eye, skin)
        body_part = self.request.GET.get("body_part")
        if body_part:
            queryset = queryset.filter(body_part=body_part)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("q", "")
        context["selected_user"] = self.request.GET.get("user", "")
        context["breeds"] = (
            Post.objects.exclude(breed=None).values_list("breed", flat=True).distinct()
        )
        context["selected_disease"] = self.request.GET.get("disease", "")
        context["selected_body_part"] = self.request.GET.get("body_part", "")
        context["diseases"] = (
            Post.objects.exclude(disease=None)
            .values_list("disease__id", "disease__name")
            .distinct()
        )
        context["users"] = Post.objects.values_list("user__id", "user__username").distinct()
        context["body_parts"] = (
            Post.objects.exclude(body_part=None).values_list("body_part", flat=True).distinct()
        )
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = "post/post_detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        user = self.request.user
        context["has_liked"] = (
            user.is_authenticated and PostLike.objects.filter(user=user, post=post).exists()
        )
        context["comment_form"] = CommentForm()
        return context


@login_required
def toggle_like(request, post_id):
    if request.method != "POST":
        return HttpResponseBadRequest("잘못된 요청입니다.")

    post = get_object_or_404(Post, id=post_id)
    user = request.user

    # PostLike를 가져오거나 없으면 생성
    like, created = PostLike.objects.get_or_create(user=user, post=post)

    if not created:
        # 이미 눌렀던 경우: 삭제
        like.delete()
        liked = False
    else:
        liked = True

    return JsonResponse(
        {
            "liked": liked,
            "like_count": post.likes.count(),  # related_name="likes" 활용
        }
    )


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        post = get_object_or_404(Post, id=self.kwargs["post_id"])
        form.instance.post = post
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("post_detail", kwargs={"pk": self.kwargs["post_id"]})
