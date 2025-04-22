from django import forms
from .models import Post, Comment
from dogs.models import Dog


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["dog", "title", "content", "image", "breed", "disease", "body_part"]
        widgets = {
            "dog": forms.Select(attrs={"class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 6}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "disease": forms.Select(attrs={"class": "form-control"}),
            "body_part": forms.Select(attrs={"class": "form-control"}),
        }
        labels = {
            "dog": "반려견",
            "title": "제목",
            "content": "내용",
            "image": "이미지",
            "disease": "질환",
            "body_part": "질환 부위",
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields["dog"].queryset = Dog.objects.filter(user=user)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content", "parent_comment"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 3, "placeholder": "댓글을 입력하세요..."}),
            "parent_comment": forms.HiddenInput(),
        }
