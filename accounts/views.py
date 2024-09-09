from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView

from .forms import UserRegisterForm
from .forms import UserLoginForm


class UserRegisterView(SuccessMessageMixin, CreateView):
    """
    View for register User
    """
    form_class = UserRegisterForm
    success_url = reverse_lazy('home')
    template_name = 'accounts/user_register.html'


class UserLoginView(SuccessMessageMixin, LoginView):
    """
    View for login User
    """
    form_class = UserLoginForm
    template_name = 'accounts/user_login.html'
    next_page = 'home'


class UserLogoutView(LogoutView):
    """
    View for logout User
    """
    next_page = 'home'
