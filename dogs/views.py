from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView

from .forms import DogForm
from .models import Dog


class DogPublicDetailView(DetailView):
    model = Dog
    template_name = "dogs/dog_detail.html"
    context_object_name = "dog"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_edit_mode"] = False
        return context


class DogCreateView(LoginRequiredMixin, CreateView):
    model = Dog
    form_class = DogForm
    template_name = "dogs/dog_form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("dog_detail", kwargs={"dog_id": self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_edit_mode"] = False
        return context


class DogUpdateView(LoginRequiredMixin, UpdateView):
    model = Dog
    form_class = DogForm
    template_name = "dogs/dog_form.html"
    pk_url_kwarg = "dog_id"
    context_object_name = "dog"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != request.user:
            return HttpResponseForbidden("수정 권한이 없습니다.")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("dog_detail", kwargs={"dog_id": self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_edit_mode"] = True
        return context
