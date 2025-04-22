from django import forms
from .models import Dog


class DogForm(forms.ModelForm):
    class Meta:
        model = Dog
        fields = [
            "name",
            "photo",
            "birth_date",
            "age",
            "gender",
            "breed",
            "weight",
            "neutered",
            "notes",
        ]
        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"}),
            "gender": forms.Select(choices=[("male", "수컷"), ("female", "암컷")]),
            "breed": forms.Select(),
            "notes": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["photo"].required = False
        self.fields["birth_date"].required = False
        self.fields["age"].required = False
        self.fields["gender"].required = False
        self.fields["weight"].required = False
        self.fields["neutered"].required = False
        self.fields["notes"].required = False
