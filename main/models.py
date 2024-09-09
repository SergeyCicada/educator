import uuid

from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.text import slugify


class Employee(models.Model):
    """
    Model for employee
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')

    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(verbose_name='URL', max_length=255, blank=True)
    thumbnail = models.ImageField(default='default.jpg',
                                  verbose_name='Изображение записи',
                                  blank=True,
                                  upload_to='images/thumbnails/%Y/%m/%d/',
                                  validators=[
                                      FileExtensionValidator(allowed_extensions=('png', 'jpg', 'webp', 'jpeg', 'gif'))]
                                  )
    birthday = models.DateField()
    education = models.CharField(max_length=255, default='Не указано')
    position = models.CharField(max_length=100)
    rank = models.CharField(max_length=50, null=True, blank=True)
    classiness = models.CharField(max_length=50, null=True, blank=True)
    number = models.CharField(max_length=50, null=True, blank=True)
    badge = models.CharField(max_length=50, null=True, blank=True)
    family_status = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    date_came_service = models.DateField(null=True, blank=True)

    def __str__(self):
        """
        Returns a string representation of the object.
        :return: a string containing the surname, name, patronymic, and position of the employee.
        """
        return f"{self.surname} {self.name} {self.patronymic} ({self.position})"

    class Meta:
        """
        Meta options for the Employee model.
        """
        ordering = ['-name']  # Default ordering by name in descending order
        indexes = [models.Index(fields=['name', 'surname', 'birthday'])]  # Index for efficient querying
        verbose_name = 'Сотрудник'  # Human-readable name for the model in singular form
        verbose_name_plural = 'Сотрудники'  # Human-readable name for the model in plural form

    def get_absolute_url(self):
        """
        Get absolute url for class instance
        """
        return reverse('employee_detail', kwargs={'slug': self.slug})

    def get_delete_url(self):
        """
        Get url on employee for delete
        """
        return reverse('employee_delete', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        """
        Checking the completion of required fields
        :param args:
        :param kwargs:
        :return:
        """
        if not self.name or not self.surname or not self.birthday or not self.position:
            raise ValidationError(
                "Пожалуйста, заполните все обязательные поля: имя, фамилия, дата рождения и должность.")

        # Форматирование даты рождения в строку
        if self.birthday:
            birthday_str = self.birthday.strftime('%Y-%m-%d')
        else:
            birthday_str = 'unknown'

        # Создание слага из фамилии, даты рождения и UUID
        unique_id = uuid.uuid4()  # Генерация уникального идентификатора
        self.slug = slugify(f"{self.surname}-{birthday_str}-{unique_id}")

        super().save(*args, **kwargs)  # Сохранение объекта
