from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView

from prediction.models import Prediction
from .forms import DogForm
from .models import Dog


class DogPublicDetailView(DetailView):
    model = Dog
    template_name = "dogs/dog_page.html"
    context_object_name = "dog"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dog = self.object

        # 이 dog로 수행된 모든 PredictionResult 를 request_id별로 그룹핑
        qs = (
            Prediction.objects
            .filter(dog=dog)
            .select_related("predicted_disease")  # foreign key 최적화
            .order_by("-created_at")
        )

        groups = {}
        for r in qs:
            grp = groups.setdefault(r.request_id, {
                "request_id": r.request_id,
                "image":   r.image.url,
                "results": [],
                "dog_name": dog.name,
                "date":   r.created_at,
            })
            grp["results"].append(r)

        # dict→list 로 변환. 최신 순 유지
        predictions = list(groups.values())

        context.update({
            "form": None,
            "is_create_mode": False,
            "is_edit_mode": False,
            "predictions": predictions,
        })
        return context


class DogCreateView(LoginRequiredMixin, CreateView):
    model = Dog
    form_class = DogForm
    template_name = "dogs/dog_page.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("dog_detail", kwargs={"pk": self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "dog": None,  # 등록 시 dog 객체 없음
                "is_create_mode": True,
                "is_edit_mode": False,
            }
        )
        return context


class DogUpdateView(LoginRequiredMixin, UpdateView):
    model = Dog
    form_class = DogForm
    template_name = "dogs/dog_page.html"
    context_object_name = "dog"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != request.user:
            return HttpResponseForbidden("수정 권한이 없습니다.")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("dog_detail", kwargs={"pk": self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "is_create_mode": False,
                "is_edit_mode": True,
            }
        )
        return context
