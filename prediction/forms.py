from django import forms
from .models import Prediction

# predictions/forms.py
from django import forms
from .models import Prediction
from dogs.models import Dog


class PredictionRequestForm(forms.Form):
    dog = forms.ModelChoiceField(
        queryset=Dog.objects.none(),
        label="반려견 선택",
        empty_label="반려견을 선택하세요",
    )
    predicted_part = forms.ChoiceField(
        choices=Prediction.BodyPart.choices,
        label="질환 부위",
    )
    image = forms.ImageField(label="질환 사진")

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["dog"].queryset = Dog.objects.filter(user=user)


class PredictionResultForm(forms.ModelForm):
    class Meta:
        model = Prediction
        fields = [
            "user",
            "dog",
            "image",
            "predicted_part",
            "predicted_disease",
            "probability",
            "is_normal",
        ]
