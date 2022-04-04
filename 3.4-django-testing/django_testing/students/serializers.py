from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from students.models import Course
from django.conf import settings


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "students")

    def validate_students(self, value):
        if len(value) > settings.MAX_STUDENTS_PER_COURSE:
            raise ValidationError(f'В группе не может быть больше {settings.MAX_STUDENTS_PER_COURSE} студентов')
        return value
