from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView

from .forms import UserRegisterForm
from .forms import UserLoginForm


class UserRegisterView(SuccessMessageMixin, CreateView):
    """
    reg
    """
    form_class = UserRegisterForm
    success_url = reverse_lazy('home')
    template_name = 'accounts/user_register.html'


class UserLoginView(SuccessMessageMixin, LoginView):
    """
    auth
    """
    form_class = UserLoginForm
    template_name = 'accounts/user_login.html'
    next_page = 'home'


class UserLogoutView(LogoutView):
    """
    logout
    """
    next_page = 'home'
