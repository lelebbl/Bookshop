from django import forms
from django.contrib.auth.forms import AuthenticationForm, \
    UserCreationForm, UserChangeForm
from .models import User
from django.core.validators import RegexValidator
from django.utils import timezone
from datetime import timedelta


class UserLoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField()
    
    
    class Meta:
        model = User
        fields = ['username', 'password']


class UserRegistrationForm(UserCreationForm):
    phone = forms.CharField(
        required=True,
        help_text='Format: +375 (29) 123-45-67',
        validators=[RegexValidator(
            regex=r'^\+375 \(?(25|29|33|44)\)? \d{3}-\d{2}-\d{2}$',
            message="Phone number must be in the format: +375 (29) 123-45-67"
        )]
    )
    birth_date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text='You must be at least 18 years old.'
    )
    city = forms.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'username', 'email',
            'phone', 'birth_date', 'city',
            'password1', 'password2',
        )

    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        today = timezone.now().date()
        age = today - birth_date
        if age < timedelta(days=365 * 18):
            raise forms.ValidationError("You must be at least 18 years old.")
        return birth_date

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'customer'
        if commit:
            user.save()
        return user


class ProfileForm(UserChangeForm):
    image = forms.ImageField(required=False)
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()
    email = forms.EmailField()
    phone = forms.CharField(required=True)
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )
    city = forms.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'image',
            'first_name',
            'last_name',
            'username',
            'email',
            'phone',
            'birth_date',
            'city',
        )

    
