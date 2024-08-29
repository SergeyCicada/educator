from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView, DeleteView, UpdateView
from django.views.generic import TemplateView

from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Employee
from .forms import AddEmployeeForm, UpdateEmployeeForm, EmployeeFilterForm


class HomePageView(TemplateView):
    template_name = 'main/home.html'


class EmployeeListView(ListView):
    model = Employee
    template_name = 'employee_list.html'
    context_object_name = 'employees'
    paginate_by = 5
    # queryset = Employee.objects.all()

    def get_context_data(self, **kwargs):
        # Получаем контекст от родительского класса
        context = super().get_context_data(**kwargs)
        # Добавляем переменную show_footer в контекст
        context['show_footer'] = False  # Отключаем футер для этого представления
        context['form'] = EmployeeFilterForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = EmployeeFilterForm(self.request.GET)

        if form.is_valid():
            patronymic_filter = form.cleaned_data.get('patronymic')
            position_filter = form.cleaned_data.get('position')
            rank_filter = form.cleaned_data.get('rank')
            education_filter = form.cleaned_data.get('education')
            classiness_filter = form.cleaned_data.get('classiness')
            family_status_filter = form.cleaned_data.get('family')

            # Применяем фильтрацию по каждому полю, если значение присутствуе
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


class EmployeeDetailView(DetailView):
    model = Employee
    template_name = 'main/employee_detail.html'
    context_object_name = 'employee'


class EmployeeCreateView(CreateView):
    model = Employee
    template_name = 'main/employee_create.html'
    form_class = AddEmployeeForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        if not username or not password:
            messages.error(self.request, 'Имя пользователя и пароль обязательны.')
            return self.form_invalid(form)

        # Создаем объект User
        user = User.objects.create_user(username=username, password=password)

        employee = form.save(commit=False)
        employee.user = user

        # Сохраняем сотрудника
        messages.success(self.request, 'Сотрудник успешно добавлен.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return super().form_invalid(form)


class EmployeeDeleteView(DeleteView):
    model = Employee
    template_name = 'main/employee_confirm_delete.html'  # Шаблон для подтверждения удаления
    context_object_name = 'employee'
    success_url = reverse_lazy('home')  # URL для перенаправления после успешного удаления

    def get_object(self, queryset=None):
        # Получаем объект по слагу
        slug = self.kwargs.get('slug')
        return get_object_or_404(Employee, slug=slug)

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Сотрудник успешно удален.')
        return super().delete(request, *args, **kwargs)


class EmployeeUpdateView(UpdateView):
    """
    Представление: обновления материала на сайте
    """
    model = Employee
    template_name = 'main/employee_update.html'
    context_object_name = 'employee'
    form_class = UpdateEmployeeForm

    def form_valid(self, form):
        messages.success(self.request, 'Сотрудник успешно обновлен.')
        return super().form_valid(form)


class EmployeeSearchView(ListView):
    model = Employee
    template_name = 'main/employee_search_result.html'  # Укажите ваш шаблон
    context_object_name = 'results'

    def get_queryset(self):
        query = self.request.GET.get('surname')  # Измените 'id' на 'surname'
        if query:
            return Employee.objects.filter(surname__icontains=query)
        return Employee.objects.none()

    def render_to_response(self, context, **response_kwargs):
        # Проверяем, является ли запрос HTMX
        if self.request.headers.get('HX-Request'):
            return render(self.request, self.template_name, context, **response_kwargs)
        return super().render_to_response(context, **response_kwargs)
