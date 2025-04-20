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

        threshold = 0.3
        is_normal = all(prob < threshold for _, prob in predictions)

        for code, prob in predictions:
            disease = DiseaseInfo.objects.get(code=code)

            result_form = PredictionResultForm(
                data={
                    "user": request.user.id,
                    "dog": dog.id,
                    "image": image,
                    "predicted_part": predicted_part,
                    "predicted_disease": disease.id,
                    "probability": prob,
                    "is_normal": is_normal,
                },
                files={"image": image},
            )

            if result_form.is_valid():
                result_form.save()
            else:
                print("예측 결과 저장 실패:", result_form.errors)

        return redirect("mypage")
