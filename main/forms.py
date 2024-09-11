from django import forms
from django.contrib.auth.models import User
from .models import Employee


class AddEmployeeForm(forms.ModelForm):
    """
    Form for adding new employee
    """
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(required=True)

    class Meta:
        model = Employee
        fields = "__all__"
        exclude = ['user']

        widgets = {
            'username': forms.TextInput(),
            'password': forms.PasswordInput(),
            'name': forms.TextInput(),
            'surname': forms.TextInput(),
            'patronymic': forms.TextInput(),
            'thumbnail': forms.ClearableFileInput(),
            'birthday': forms.DateInput(),
            'position': forms.TextInput(),
            'rank': forms.TextInput(),
            'classiness': forms.TextInput(),
            'number': forms.TextInput(),
            'badge': forms.TextInput(),
            'family_status': forms.TextInput(),
            'phone_number': forms.TextInput(),
            'email': forms.EmailInput(),
            'date_came_service': forms.DateInput(),
        }

    def clean_username(self):
        """
        Checks the uniqueness of the username.
        If the username already exists in the database, a validation error is raised.
        :return: username
        """
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Этот логин уже занят. Пожалуйста, выберите другой.")
        return username

    def clean(self):
        """
        This method checks if the 'username' and 'password' fields are filled.
        If either field is empty, a validation error is added to the respective field.
        :return:
        """
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if not username:
            self.add_error('username', "Это поле обязательно для заполнения.")
        if not password:
            self.add_error('password', "Это поле обязательно для заполнения.")

        return cleaned_data


class UpdateEmployeeForm(forms.ModelForm):
    """
    Form for updating employee
    """
    class Meta:
        model = Employee
        fields = "__all__"
        exclude = ['user']

        widgets = {
            'name': forms.TextInput(),
            'surname': forms.TextInput(),
            'patronymic': forms.TextInput(),
            'thumbnail': forms.ClearableFileInput(),
            'birthday': forms.DateInput(),
            'education':  forms.TextInput(),
            'position': forms.TextInput(),
            'rank': forms.TextInput(),
            'classiness': forms.TextInput(),
            'number': forms.TextInput(),
            'badge': forms.TextInput(),
            'family_status': forms.TextInput(),
            'phone_number': forms.TextInput(),
            'email': forms.EmailInput(),
            'date_came_service': forms.DateInput(),
        }


class EmployeeFilterForm(forms.Form):
    """
    Filter for search employee in employee list
    """
    position = forms.CharField(required=False)
    rank = forms.CharField(required=False)
    education = forms.CharField(required=False)
    classiness = forms.CharField(required=False)
    family_status = forms.CharField(required=False)
