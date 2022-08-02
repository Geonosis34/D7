from django.forms import BooleanField, ChoiceField
from django import forms
from .models import News, Category
from django.core.exceptions import ValidationError

class NewsForm(forms.ModelForm):
    check_box = BooleanField(label='Согласен!')
    description = forms.CharField(min_length=20)

    class Meta:
       model = News
       fields = [
           'name',
           'description',
           'category',
           'author',
       ]

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        description = cleaned_data.get("description")

        if name == description:
            raise ValidationError(
                "Имя статьи и описание статьи должны отличаться!"
            )
        return cleaned_data




