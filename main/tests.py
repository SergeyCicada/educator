from django.test import TestCase, SimpleTestCase
from django.urls import reverse
from django.urls.base import resolve

from django.contrib.auth.models import User

from .models import Employee
from .views import EmployeeListView, EmployeeSearchView, EmployeeCreateView, EmployeeDetailView, EmployeeDeleteView, \
    EmployeeUpdateView
from .forms import AddEmployeeForm


from django.test import TestCase
from django.contrib.auth.models import User
from .models import Employee
from django.core.exceptions import ValidationError
from datetime import date


class EmployeeURLsTest(TestCase):
    """
    Test for URLs main (Employee)
    """

    def setUp(self):
        # Create test User
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_employee_list_url(self):
        # Test for get status code 200 (employee_list)
        response = self.client.get(reverse('employee_list'))
        self.assertEqual(response.status_code, 200)

    def test_root_url_resolves_to_employee_list_view(self):
        # Test for matching url and view employee_list
        found = resolve('/employees/')
        self.assertEqual(found.func.view_class, EmployeeListView)

    def test_employee_search_url(self):
        # Test for get status code 200 (employee_search)
        response = self.client.get(reverse('employee_search'))
        self.assertEqual(response.status_code, 200)

    def test_root_url_resolves_to_employee_search_view(self):
        # Test for matching url and view employee_search
        found = resolve('/employees/search/')
        self.assertEqual(found.func.view_class, EmployeeSearchView)

    def test_employee_create_url(self):
        # Test for get status code 200 (employee_create)
        response = self.client.get(reverse('employee_create'))
        self.assertEqual(response.status_code, 200)

    def test_root_url_resolves_to_employee_create_view(self):
        # Test for matching url and view employee_create
        found = resolve('/employees/create/')
        self.assertEqual(found.func.view_class, EmployeeCreateView)

    def test_employee_detail_url(self):
        # Test for get status code 200 (employee_detail)
        response = self.client.get(reverse('employee_detail'))
        self.assertEqual(response.status_code, 200)

    def test_root_url_resolves_to_employee_detail_view(self):
        # Test for matching url and view employee_detail
        found = resolve('/employees/<slug:slug>/')
        self.assertEqual(found.func.view_class, EmployeeDetailView)

    def test_employee_employee_delete(self):
        # Test for get status code 200 (employee_delete)
        response = self.client.get(reverse('employee_delete'))
        self.assertEqual(response.status_code, 200)

    def test_root_url_resolves_to_employee_delete_view(self):
        # Test for matching url and view employee_delete
        found = resolve('/employees/<slug:slug>/delete/')
        self.assertEqual(found.func.view_class, EmployeeDeleteView)

    def test_employee_update_url(self):
        # Test for get status code 200 (employee_update)
        response = self.client.get(reverse('employee_update'))
        self.assertEqual(response.status_code, 200)

    def test_root_url_resolves_to_employee_update_view(self):
        # Test for matching url and view employee_update
        found = resolve('/employees/create/')
        self.assertEqual(found.func.view_class, EmployeeUpdateView)


class EmployeeModelTests(TestCase):
    """
    Tests for model Employee
    """
    def setUp(self):
        # Create a user for relate with Employee
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_create_employee(self):
        # Test for Employee with valid data
        employee = Employee.objects.create(
            user=self.user,
            name='Иван',
            surname='Иванов',
            birthday=date(1990, 1, 1),
            position='Менеджер'
        )
        self.assertEqual(employee.name, 'Иван')
        self.assertEqual(employee.surname, 'Иванов')
        self.assertEqual(employee.position, 'Менеджер')
        self.assertIsNotNone(employee.slug)  # Check generate slug

    def test_employee_str(self):
        # Test for str employee
        employee = Employee.objects.create(
            user=self.user,
            name='Иван',
            surname='Иванов',
            birthday=date(1990, 1, 1),
            position='Менеджер'
        )
        self.assertEqual(str(employee), 'Иванов Иван None (Менеджер)')

    def test_save_employee_without_required_fields(self):
        # Test for create an employee without required fields
        employee = Employee(user=self.user)
        with self.assertRaises(ValidationError):
            employee.save()
            employee.full_clean()

    def test_get_absolute_url(self):
        # Test for get absolute URL employee
        employee = Employee.objects.create(
            user=self.user,
            name='Иван',
            surname='Иванов',
            birthday=date(1990, 1, 1),
            position='Менеджер'
        )
        expected_url = f"/employees/{employee.slug}/"
        self.assertEqual(employee.get_absolute_url(), expected_url)

    def test_get_delete_url(self):
        # Test for get URL delete employee
        employee = Employee.objects.create(
            user=self.user,
            name='Иван',
            surname='Иванов',
            birthday=date(1990, 1, 1),
            position='Менеджер'
        )
        expected_delete_url = f"/employees/{employee.slug}/delete/"
        self.assertEqual(employee.get_delete_url(), expected_delete_url)

    def test_slug_generation(self):
        # Test for generation slug when save employee
        employee = Employee.objects.create(
            user=self.user,
            name='Иван',
            surname='Иванов',
            birthday=date(1990, 1, 1),
            position='Менеджер'
        )
        self.assertIsNotNone(employee.slug)




