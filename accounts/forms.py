from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm


class UserRegisterForm(UserCreationForm):
    fields = UserCreationForm.Meta.fields

    def __init__(self, *args, **kwargs):
        """
        Updating style for form register
        """
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({"placeholder": "Придумайте свой логин"})
        self.fields['password1'].widget.attrs.update({"placeholder": "Придумайте свой пароль"})
        self.fields['password2'].widget.attrs.update({"placeholder": "Повторите придуманный пароль"})
        for field in self.fields:
            self.fields[field].widget.attrs.update({"autocomplete": "off"})
        self.fields['username'].error_messages = {
            'required': 'Это поле обязательно для заполнения.',
        }
        self.fields['password1'].error_messages = {
            'required': 'Это поле обязательно для заполнения.',
        }
        self.fields['password2'].error_messages = {
            'required': 'Это поле обязательно для заполнения.',
        }


class UserLoginForm(AuthenticationForm):
    """
    Form for UserLogin
    """

    def __init__(self, *args, **kwargs):
        """
        Updating style form for UserLogin
        """
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Логин пользователя'
        self.fields['password'].widget.attrs['placeholder'] = 'Пароль пользователя'
        self.fields['username'].label = 'Логин'
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })
        self.fields['username'].error_messages = {
            'required': 'Это поле обязательно для заполнения.',
        }
        self.fields['password'].error_messages = {
            'required': 'Это поле обязательно для заполнения.',
        }
