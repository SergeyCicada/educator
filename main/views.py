from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView, DeleteView, UpdateView
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from .forms import AddEmployeeForm, UpdateEmployeeForm, EmployeeFilterForm
from django.views.generic.edit import CreateView
from django.contrib import messages
from .models import Employee
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin


class HomePageView(LoginRequiredMixin, TemplateView):
    """
    View for path('', HomePageView.as_view(), name='home'),
    """
    template_name = 'main/home.html'
    login_url = 'login'


class EmployeeListView(LoginRequiredMixin, ListView):
    """
    View for path('', EmployeeListView.as_view(), name='employee_list')
    """
    model = Employee
    template_name = 'main/employee_list.html'
    context_object_name = 'employees'
    paginate_by = 5
    login_url = 'login'

    def get_queryset(self):
        queryset = super().get_queryset()
        form = EmployeeFilterForm(self.request.GET)

        if form.is_valid():
            patronymic_filter = form.cleaned_data.get('patronymic')
            position_filter = form.cleaned_data.get('position')
            rank_filter = form.cleaned_data.get('rank')
            education_filter = form.cleaned_data.get('education')
            classiness_filter = form.cleaned_data.get('classiness')
            family_status_filter = form.cleaned_data.get('family_status')

            if patronymic_filter:
                queryset = queryset.filter(patronymic__icontains=patronymic_filter)
            if position_filter:
                queryset = queryset.filter(position__icontains=position_filter)
            if rank_filter:
                queryset = queryset.filter(rank__icontains=rank_filter)
            if education_filter:
                queryset = queryset.filter(education__icontains=education_filter)
            if classiness_filter:
                queryset = queryset.filter(classiness__icontains=classiness_filter)
            if family_status_filter:
                queryset = queryset.filter(family_status__icontains=family_status_filter)

        return queryset

    def get(self, request, *args, **kwargs):
        """If the request is an AJAX request, it returns the rendered template."""
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            self.object_list = self.get_queryset()
            context = self.get_context_data()
            return render(request, self.template_name, context)
        return super().get(request, *args, **kwargs)


class EmployeeDetailView(LoginRequiredMixin, DetailView):
    """
    View for path('<slug:slug>/', EmployeeDetailView.as_view(), name='employee_detail'),
    """
    model = Employee
    template_name = 'main/employee_detail.html'
    context_object_name = 'employee'
    login_url = 'login'


class EmployeeCreateView(LoginRequiredMixin, CreateView):
    """
    View for path('create/', EmployeeCreateView.as_view(), name='employee_create'),
    """
    model = Employee
    template_name = 'main/employee_create.html'
    form_class = AddEmployeeForm
    success_url = reverse_lazy('employee_list')
    login_url = 'login'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        if not username or not password:
            messages.error(self.request, 'Имя пользователя и пароль обязательны.')
            return self.form_invalid(form)

        user = User.objects.create_user(username=username, password=password)

        employee = form.save(commit=False)
        employee.user = user

        employee.save()
        messages.success(self.request, 'Сотрудник успешно добавлен.')

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')

        return super().form_invalid(form)


class EmployeeDeleteView(LoginRequiredMixin, DeleteView):
    """
    View for path('<slug:slug>/delete/', EmployeeDeleteView.as_view(), name='employee_delete'),,
    """
    model = Employee
    template_name = 'main/employee_confirm_delete.html'  # Шаблон для подтверждения удаления
    context_object_name = 'employee'
    success_url = reverse_lazy('home')  # URL для перенаправления после успешного удаления
    login_url = 'login'

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Employee, slug=slug)

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class EmployeeUpdateView(LoginRequiredMixin, UpdateView):
    """
    View for  path('<slug:slug>/update/', EmployeeUpdateView.as_view(), name='employee_update')
    """
    model = Employee
    template_name = 'main/employee_update.html'
    context_object_name = 'employee'
    form_class = UpdateEmployeeForm

    def form_valid(self, form):
        messages.success(self.request, 'Сотрудник успешно обновлен.')
        return super().form_valid(form)


class EmployeeSearchView(LoginRequiredMixin, ListView):
    """
    View for EmployeeSearch path('search/', EmployeeSearchView.as_view(), name='employee_search'),
    """
    model = Employee
    template_name = 'main/employee_search_result.html'
    context_object_name = 'results'

    def get_queryset(self):
        query = self.request.GET.get('surname')
        if query:
            return Employee.objects.filter(surname__icontains=query)
        return Employee.objects.none()

    def render_to_response(self, context, **response_kwargs):
        # Проверяем, является ли запрос HTMX
        if self.request.headers.get('HX-Request'):
            return render(self.request, self.template_name, context, **response_kwargs)
        return super().render_to_response(context, **response_kwargs)
