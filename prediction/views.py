import uuid
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PredictionRequestForm, PredictionResultForm
from .models import DiseaseInfo, Prediction
from .utils import run_diagnosis


class PredictionCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = PredictionRequestForm(user=request.user)
        return render(request, "prediction/prediction_form.html", {"form": form})

    def post(self, request):
        form = PredictionRequestForm(request.POST, request.FILES, user=request.user)
        if not form.is_valid():
            return render(request, "prediction/prediction_form.html", {"form": form})

        dog = form.cleaned_data["dog"]
        image = form.cleaned_data["image"]
        predicted_part = form.cleaned_data["predicted_part"]

        predictions = run_diagnosis(img=image, part=predicted_part)
        image.seek(0)

        threshold = 0.3
        is_normal = all(prob < threshold for _, prob in predictions)

        request_id = uuid.uuid4()

        for code, prob in predictions:
            disease = DiseaseInfo.objects.get(code=code)
            image.seek(0)

            result_form = PredictionResultForm(
                data={
                    "user": request.user.id,
                    "dog": dog.id,
                    "predicted_part": predicted_part,
                    "predicted_disease": disease.id,
                    "probability": prob,
                    "is_normal": is_normal,
                    "request_id": request_id,
                },
                files={"image": image},
            )

            if result_form.is_valid():
                result_form.save()
            else:
                print("예측 결과 저장 실패:", result_form.errors)

        return redirect("prediction_result", request_id=request_id)


class PredictionResultView(LoginRequiredMixin, View):
    def get(self, request, request_id):
        predictions = Prediction.objects.filter(
            user=request.user, request_id=request_id
        ).select_related("predicted_disease", "dog")

        if not predictions.exists():
            return redirect("prediction_create")

        # dog, part, created_at 은 동일하므로 하나만 대표로 뽑음
        dog = predictions[0].dog
        part = predictions[0].predicted_part
        created_at = predictions[0].created_at

        return render(
            request,
            "prediction/prediction_result.html",
            {
                "dog": dog,
                "part": part,
                "created_at": created_at,
                "predictions": predictions,
            },
        )
