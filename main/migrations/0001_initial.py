# Generated by Django 5.1 on 2024-08-19 21:37

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('surname', models.CharField(max_length=100)),
                ('patronymic', models.CharField(blank=True, max_length=100, null=True)),
                ('slug', models.SlugField(blank=True, max_length=255, verbose_name='URL')),
                ('thumbnail', models.ImageField(blank=True, default='media/images/default.jpg', upload_to='images/thumbnails/%Y/%m/%d/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=('png', 'jpg', 'webp', 'jpeg', 'gif'))], verbose_name='Изображение записи')),
                ('birthday', models.DateField()),
                ('position', models.CharField(max_length=100)),
                ('rank', models.CharField(blank=True, max_length=50, null=True)),
                ('classiness', models.CharField(blank=True, max_length=50, null=True)),
                ('number', models.CharField(blank=True, max_length=50, null=True)),
                ('badge', models.CharField(blank=True, max_length=50, null=True)),
                ('family_status', models.CharField(blank=True, max_length=50, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('date_came_service', models.DateField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='employee_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Сотрудник',
                'verbose_name_plural': 'Сотрудники',
                'ordering': ['-name'],
                'indexes': [models.Index(fields=['name', 'surname', 'birthday'], name='main_employ_name_5c7adf_idx')],
            },
        ),
    ]
