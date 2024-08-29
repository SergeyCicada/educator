import uuid

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from services.utils import unique_slugify


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')

    name = models.CharField(max_length=100)  # Фамилия
    surname = models.CharField(max_length=100)  # Имя
    patronymic = models.CharField(max_length=100, null=True, blank=True)  # Отчество
    slug = models.SlugField(verbose_name='URL', max_length=255, blank=True)  # Url
    thumbnail = models.ImageField(default='default.jpg',
                                  verbose_name='Изображение записи',
                                  blank=True,
                                  upload_to='images/thumbnails/%Y/%m/%d/',
                                  validators=[
                                      FileExtensionValidator(allowed_extensions=('png', 'jpg', 'webp', 'jpeg', 'gif'))]
                                  )
    birthday = models.DateField()  # Дата рождения
    education = models.CharField(max_length=255, default='Не указано')  # Образование
    position = models.CharField(max_length=100)  # Должность
    rank = models.CharField(max_length=50, null=True, blank=True)  # Звание
    classiness = models.CharField(max_length=50, null=True, blank=True)  # Классность
    number = models.CharField(max_length=50, null=True, blank=True)  # Номер
    badge = models.CharField(max_length=50, null=True, blank=True)  # Значок
    family_status = models.CharField(max_length=50, null=True, blank=True)  # Семейное положение
    phone_number = models.CharField(max_length=15, null=True, blank=True)  # Номер телефона
    email = models.EmailField(null=True, blank=True)  # Электронная почта
    date_came_service = models.DateField(null=True, blank=True)  # Дата поступления на службу

    def __str__(self):
        return f"{self.surname} {self.name} {self.patronymic} ({self.position})"

    class Meta:
        ordering = ['-name']
        indexes = [models.Index(fields=['name', 'surname', 'birthday'])]
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def get_absolute_url(self):
        """
        get url on employee
        """
        return reverse('employee_detail', kwargs={'slug': self.slug})

    def get_delete_url(self):
        """
        get url on employee for delete
        """
        return reverse('employee_delete', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        # Проверка обязательных полей
        if not self.name or not self.surname or not self.birthday or not self.position:
            raise ValidationError(
                "Пожалуйста, заполните все обязательные поля: имя, фамилия, дата рождения и должность.")

        # Форматирование даты рождения в строку
        if self.birthday:
            birthday_str = self.birthday.strftime('%Y-%m-%d')  # Формат: ГГГГ-ММ-ДД
        else:
            birthday_str = 'unknown'  # На случай, если дата рождения не указана

        # Создание слага из фамилии, даты рождения и UUID
        unique_id = uuid.uuid4()  # Генерация уникального идентификатора
        self.slug = slugify(f"{self.surname}-{birthday_str}-{unique_id}")

        super().save(*args, **kwargs)  # Сохранение объекта
