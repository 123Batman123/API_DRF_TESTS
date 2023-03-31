from rest_framework import serializers
#from rest_framework.exceptions import ValidationError
from students.models import Course


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "students")

    # def validate(self, data):
    #     obj = Course.objects.all()
    #     if obj[0].students.count() > 5:
    #         raise ValidationError('Больше 5 курсов!')
    #     return data
