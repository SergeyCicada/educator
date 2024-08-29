from django.urls import path

from .views import EmployeeListView, EmployeeDetailView, EmployeeCreateView, EmployeeDeleteView, EmployeeUpdateView, EmployeeSearchView



urlpatterns = [

    path('', EmployeeListView.as_view(), name='home'),
    path('search/', EmployeeSearchView.as_view(), name='employee_search'),
    path('create/', EmployeeCreateView.as_view(), name='employee_create'),
    path('<slug:slug>/', EmployeeDetailView.as_view(), name='employee_detail'),
    path('<slug:slug>/delete/', EmployeeDeleteView.as_view(), name='employee_delete'),
    path('<slug:slug>/update/', EmployeeUpdateView.as_view(), name='employee_update')

]
