from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView

from .models import Post
from .forms import PostForm


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
