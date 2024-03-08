from django import forms
from django.core.exceptions import ValidationError
from .models import Review


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ["review"]
        widgets = {
            'review': forms.TextInput(attrs={'class': 'class-input'})
        }

    def clean_review(self):
        review = self.cleaned_data['review']
        if len(review) < 5:
            raise ValidationError("Пожалуйста по длинее")
        return review
