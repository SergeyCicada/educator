from django import forms
from django.contrib.auth.models import User
from .models import Employee
from datetime import datetime


class AddEmployeeForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True, label='Имя пользователя')
    password = forms.CharField(widget=forms.PasswordInput, required=True, label='Пароль')

    class Meta:
        model = Employee
        fields = "__all__"
        exclude = ['user']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'patronymic': forms.TextInput(attrs={'class': 'form-control'}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'birthday': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}  # Используем тип date
            ),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'rank': forms.TextInput(attrs={'class': 'form-control'}),
            'classiness': forms.TextInput(attrs={'class': 'form-control'}),
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'badge': forms.TextInput(attrs={'class': 'form-control'}),
            'family_status': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'date_came_service': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}  # Используем тип date
            ),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Этот логин уже занят. Пожалуйста, выберите другой.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if not username:
            self.add_error('username', "Это поле обязательно для заполнения.")
        if not password:
            self.add_error('password', "Это поле обязательно для заполнения.")

        return cleaned_data


class UpdateEmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = "__all__"
        exclude = ['user']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'patronymic': forms.TextInput(attrs={'class': 'form-control'}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'birthday': forms.DateInput(),
            'education':  forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'rank': forms.TextInput(attrs={'class': 'form-control'}),
            'classiness': forms.TextInput(attrs={'class': 'form-control'}),
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'badge': forms.TextInput(attrs={'class': 'form-control'}),
            'family_status': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form'}),
            'date_came_service': forms.DateInput(),
        }


class EmployeeFilterForm(forms.Form):
    position = forms.CharField(required=False, label='Должность', widget=forms.TextInput(attrs={'class': 'form-control'}))
    rank = forms.CharField(required=False, label='Звание', widget=forms.TextInput(attrs={'class': 'form-control'}))
    education = forms.CharField(required=False, label='Образование', widget=forms.TextInput(attrs={'class': 'form-control'}))
    classiness = forms.CharField(required=False, label='Классность', widget=forms.TextInput(attrs={'class': 'form-control'}))
    family_status = forms.CharField(required=False, label='Семейное положение', widget=forms.TextInput(attrs={'class': 'form-control'}))
