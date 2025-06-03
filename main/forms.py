from django import forms
from .models import Review, Category, Product  

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Напишите отзыв...'}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Название категории'}),
            'slug': forms.TextInput(attrs={'placeholder': 'Slug (например, electronics)'}),
        }
        

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'slug', 'category', 'image', 'description', 'price', 'discount', 'available']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Название товара'}),
            'slug': forms.TextInput(attrs={'placeholder': 'slug'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'price': forms.NumberInput(attrs={'step': 0.01}),
            'discount': forms.NumberInput(attrs={'step': 0.01, 'max': 100}),
        }
