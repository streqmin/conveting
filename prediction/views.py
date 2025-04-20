from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PredictionRequestForm, PredictionResultForm
from .models import DiseaseInfo
from .utils import run_diagnosis


class PredictionCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = PredictionRequestForm(user=request.user)
        return render(request, "predictions/prediction_form.html", {"form": form})

    def post(self, request):
        form = PredictionRequestForm(request.POST, request.FILES, user=request.user)
        if not form.is_valid():
            return render(request, "predictions/prediction_form.html", {"form": form})

        dog = form.cleaned_data["dog"]
        image = form.cleaned_data["image"]
        predicted_part = form.cleaned_data["predicted_part"]

        predictions = run_diagnosis(image=image, part=predicted_part)

        for pred in predictions:
            disease = DiseaseInfo.objects.get(code=pred["code"])

            result_form = PredictionResultForm(
                data={
                    "user": request.user.id,
                    "dog": dog.id,
                    "image": image,
                    "predicted_part": predicted_part,
                    "predicted_disease": disease.id,
                    "probability": pred["probability"],
                    "is_normal": False,
                },
                files={"image": image},
            )

            if result_form.is_valid():
                result_form.save()
            else:
                # 폼 유효성 실패 시 로그 남기거나 처리
                print("예측 결과 저장 실패:", result_form.errors)

        return redirect("mypage")
