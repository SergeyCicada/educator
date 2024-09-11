from django.test import TestCase, SimpleTestCase
from django.urls import reverse
from django.urls.base import resolve

from django.contrib.auth.models import User

from .models import Employee
from .views import EmployeeListView
from .forms import AddEmployeeForm


class EmployeeViewTests(TestCase):
    """
    Tests for views
    """
    def test_employee_list_view(self):
        # Create user for first employee
        user_1 = User.objects.create_user(
            username='ivanov',
            password='password123',
            email='ivanov@example.com'
        )

        Employee_1 = Employee.objects.create(
            user=user_1,
            name='Иван',
            surname='Иванов',
            patronymic='Иванович',
            position='Старший инспектор',
            birthday='1990-01-01',
            rank='Майор',
            classiness='1 класс',
            number='12345',
            badge='Значок 1',
            family_status='Женат',
            phone_number='1234567890',
            date_came_service='2010-01-01'
        )
        # Create user for second employee
        user_2 = User.objects.create_user(
            username='petrov',
            password='password123',
            email='petrov@example.com'
        )

        Employee_2 = Employee.objects.create(
            user=user_2,
            name='Петр',
            firstname='Петров',
            patronymic='Петрович',
            position='Младший инспектор',
            birthday='1999-05-05',
            rank='Старший лейтенант',
            classiness='3 класс',
            number='5885',
            badge='Значок 3',
            family_status='Не женат',
            phone_number='098765543',
            date_came_service='2016-06-06',
        )

        response = self.client.get(reverse('home'))

        self.assertIn('Иванов Иван Иванович', response.content.decode())
        self.assertIn('Петров Петр Петрович', response.content.decode())


class EmployeeTemplateTests(TestCase):
    """Tests template"""
    def test_homepage_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'main/employee_list.html')

    def test_homepage_contains_correct_html(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Educator')

    def test_homepage_does_not_contain_incorrect_html(self):
        response = self.client.get(reverse('home'))
        self.assertNotContains(response, 'Hello World!')


# class EmployeeFormTests(TestCase):
#     """Tests for forms"""
#     def setUp(self):
#         url = reverse('home')
#         self.response = self.client.get(url)
#
#     def test_employee_form(self):
#         form = self.response.context.get('add_employee_form')
#         self.assertIsInstance(form, AddEmployeeForm)
#         self.assertContains(self.response, 'csrfmiddlewaretoken')
#
#     def test_employee_form_validation_for_blank_items(self):
#         add_book_form = AddEmployeeForm(
#             data={'name': '', 'firstname': '', 'position': '', 'birthday': ''}
#         )
#         self.assertFalse(add_book_form.is_valid())


class EmployeeURLsTest(TestCase):
    """Testing URLs"""

    def test_homepage_url_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_root_url_resloves_to_homepage_view(self):
        found = resolve('/')
        self.assertEqual(found.func.view_class, EmployeeListView)


class EmployeeModelTests(TestCase):
    """Tests for model Employee"""
    def setUp(self):
        # Create user for test
        self.user = User.objects.create_user(username='test_user', password='testpass')

        # Create Employee
        self.employee = Employee.objects.create(
            user=self.user,
            name='Иван',
            surname='Иванов',
            patronymic='Иванович',
            position='Старший инспектор',
            birthday='1990-01-01',
            rank='Майор',
            classiness='1 класс',
            number='12345',
            badge='Значок 1',
            family_status='Женат',
            phone_number='1234567890',
            email='ivanov@example.com',
            date_came_service='2010-01-01'
        )

    def test_create_employee(self):
        # Checking employee creation
        self.assertIsInstance(self.employee, Employee)

    def test_str_representation(self):
        # Checking return self.employee
        self.assertEqual(str(self.employee), "Иванов Иван Иванович (Старший инспектор)")

    def test_saving_and_retrieving_book(self):
        # Create user for first and second second employee
        first_user = User.objects.create_user(username='test_user_1', password='testpass')
        second_user = User.objects.create_user(username='test_user_2', password='testpass')

        first_employee = Employee()
        first_employee.user = first_user
        first_employee.name = 'Иванов'
        first_employee.firstname = 'Иван'
        first_employee.patronymic = 'Иванович'
        first_employee.position = 'Старший инспектор'
        first_employee.birthday = '1990-01-01'
        first_employee.rank = 'Майор'
        first_employee.classiness = '1 класс'
        first_employee.number = '12345'
        first_employee.badge = 'Значок 1'
        first_employee.family_status = 'Женат'
        first_employee.phone_number = '1234567890'
        first_employee.email = 'ivanov@example.com'
        first_employee.date_came_service = '2010-01-01'
        first_employee.save()

        second_employee = Employee()
        second_employee.user = second_user
        second_employee.name = 'Петров'
        second_employee.firstname = 'Петр'
        second_employee.patronymic = 'Петрович'
        second_employee.position = 'Младший инспектор'
        second_employee.birthday = '1999-05-05'
        second_employee.rank = 'Старший лейтенант'
        second_employee.classiness = '3 класс'
        second_employee.number = '5885'
        second_employee.badge = 'Значок 3'
        second_employee.family_status = 'Не женат'
        second_employee.phone_number = '098765543'
        second_employee.email = 'petrov@example.com'
        second_employee.date_came_service = '2016-06-06'
        second_employee.save()

        # Checking that two employees are saved
        saved_first_employee = Employee.objects.get(firstname='Иван')
        saved_second_employee = Employee.objects.get(firstname='Петр')

        # Ckecking data first employee
        self.assertEqual(saved_first_employee.name, 'Иванов')
        self.assertEqual(saved_first_employee.firstname, 'Иван')
        self.assertEqual(saved_first_employee.patronymic, 'Иванович')
        self.assertEqual(saved_first_employee.position, 'Старший инспектор')
        self.assertEqual(saved_first_employee.rank, 'Майор')
        self.assertEqual(saved_first_employee.classiness, '1 класс')
        self.assertEqual(saved_first_employee.number, '12345')
        self.assertEqual(saved_first_employee.badge, 'Значок 1')
        self.assertEqual(saved_first_employee.family_status, 'Женат')
        self.assertEqual(saved_first_employee.phone_number, '1234567890')
        self.assertEqual(saved_first_employee.email, 'ivanov@example.com')
        self.assertEqual(str(saved_first_employee.date_came_service), '2010-01-01')

        # Ckecking data second employee
        self.assertEqual(saved_second_employee.name, 'Петров')
        self.assertEqual(saved_second_employee.firstname, 'Петр')
        self.assertEqual(saved_second_employee.patronymic, 'Петрович')
        self.assertEqual(saved_second_employee.position, 'Младший инспектор')
        self.assertEqual(saved_second_employee.rank, 'Старший лейтенант')
        self.assertEqual(saved_second_employee.classiness, '3 класс')
        self.assertEqual(saved_second_employee.number, '5885')
        self.assertEqual(saved_second_employee.badge, 'Значок 3')
        self.assertEqual(saved_second_employee.family_status, 'Не женат')
        self.assertEqual(saved_second_employee.phone_number, '098765543')
        self.assertEqual(saved_second_employee.email, 'petrov@example.com')
        self.assertEqual(str(saved_second_employee.date_came_service), '2016-06-06')




