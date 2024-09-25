from datetime import date

from django.test import TestCase, SimpleTestCase
from django.urls import reverse
from django.urls.base import resolve

from django.contrib.auth.models import User
from main.models import Employee
from main.views import EmployeeListView, EmployeeSearchView, EmployeeCreateView, EmployeeDetailView, EmployeeDeleteView, \
    EmployeeUpdateView
from main.forms import AddEmployeeForm, UpdateEmployeeForm, EmployeeFilterForm


class AddEmployeeFormTests(TestCase):
    """
    Tests for forms
    """
    def setUp(self):
        # Create test user and login, get form.
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        url = reverse('employee_create')
        self.response = self.client.get(url)

    def test_book_form(self):
        # Check type form and csrf
        self.assertEqual(self.response.status_code, 200)
        form = self.response.context.get('form')
        self.assertIsInstance(form, AddEmployeeForm)  # type form
        self.assertContains(self.response, 'csrfmiddlewaretoken')  # csrf

    def test_book_form_validation_for_blank_items(self):
        # Check validation form, return false if fields are empty
        add_book_form = AddEmployeeForm(
            data={'username': '',
                  'password': '',
                  'name': '',
                  'surname': '',
                  'patronymic': '',
                  'thumbnail': '',
                  'birthday': '',
                  'position': '',
                  'rank': '',
                  'classiness': '',
                  'number': '',
                  'badge': '',
                  'family_status': '',
                  'phone_number': '',
                  'email': '',
                  'date_came_service': ''}
        )
        self.assertFalse(add_book_form.is_valid())


class UpdateEmployeeFormTests(TestCase):
    """
    Tests for forms
    """
    def setUp(self):
        # Create test user and login, create employee, get form.
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        employee = Employee.objects.create(
            user=self.user,
            name='Иван',
            surname='Иванов',
            birthday=date(1990, 1, 1),
            position='Менеджер'
        )
        slug_value = employee.slug
        url = reverse('employee_update', kwargs={'slug': slug_value})
        self.response = self.client.get(url)

    def test_book_form(self):
        # Check type form and csrf
        self.assertEqual(self.response.status_code, 200)
        form = self.response.context.get('form')
        self.assertIsInstance(form, UpdateEmployeeForm)  # type form
        self.assertContains(self.response, 'csrfmiddlewaretoken')  # csrf

    def test_book_form_validation_for_blank_items(self):
        # Check validation form, return false if fields are empty
        add_book_form = UpdateEmployeeForm(
            data={'username': '',
                  'password': '',
                  'name': '',
                  'surname': '',
                  'patronymic': '',
                  'thumbnail': '',
                  'birthday': '',
                  'position': '',
                  'rank': '',
                  'classiness': '',
                  'number': '',
                  'badge': '',
                  'family_status': '',
                  'phone_number': '',
                  'email': '',
                  'date_came_service': ''}
        )
        self.assertFalse(add_book_form.is_valid())


class FilterEmployeeListViewTests(TestCase):
    """
    Tests for EmployeeListView
    """
    def setUp(self):
        # Create user for employees
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user2 = User.objects.create_user(username='testuser2', password='testpass2')
        self.client.login(username='testuser', password='testpass')

        # Create employees
        self.employee1 = Employee.objects.create(
            user=self.user,
            name='Ivan',
            surname='Ivanov',
            patronymic='Ivanovich',
            position='Manager',
            rank='Senior',
            education='Master',
            classiness='A',
            family_status='Single',
            birthday=date(1990, 1, 1)
        )
        self.employee2 = Employee.objects.create(
            user=self.user2,
            name='Petr',
            surname='Petrov',
            patronymic='Petrovich',
            position='Developer',
            rank='Junior',
            education='Bachelor',
            classiness='B',
            family_status='Married',
            birthday=date(1992, 2, 2)
        )

    def test_filter_by_position(self):
        # Filter test by position
        url = reverse('employee_list') + '?position=Manager'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ivanovich')
        self.assertNotContains(response, 'Petrovich')

    def test_filter_by_rank(self):
        # Filter test by rank
        url = reverse('employee_list') + '?rank=Senior'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ivanovich')
        self.assertNotContains(response, 'Petrovich')

    def test_no_filter(self):
        # Test without filters
        url = reverse('employee_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ivanovich')
        self.assertContains(response, 'Petrovich')


class EmployeeTemplateHomeTests(TestCase):
    """
    Tests for templates
    """

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        url = reverse('home')
        self.response = self.client.get(url)

    def test_homepage_template(self):
        self.assertTemplateUsed(self.response, 'main/home.html')


class EmployeeTemplateSearchTests(TestCase):
    """
    Tests for templates
    """

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        url = reverse('employee_search')
        self.response = self.client.get(url)

    def test_homepage_template(self):
        self.assertTemplateUsed(self.response, 'main/employee_search_result.html')
