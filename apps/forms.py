
from django import forms
from .models import Category, Product


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'icon', 'slug')
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "icon": forms.URLInput(attrs={"class": "form-control"}),
        }






