from rest_framework import serializers
from main.models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'user',
            'name',
            'surname',
            'patronymic',
            'slug',
            'thumbnail',
            'birthday',
            'education',
            'position',
            'rank',
            'classiness',
            'number',
            'badge',
            'family_status',
            'phone_number',
            'email',
            'date_came_service',
        )
        model = Employee
