from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField, StringRelatedField
from learning.models import Course
from auth_app.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'last_name', )

    def to_representation(self, instance):
        return f'{instance.first_name} {instance.last_name}'


class CourseSerializer(ModelSerializer):
    authors = UserSerializer(many=True)

    class Meta:
        model = Course
        fields = (
            'id',
            'title',
            'price',
            'authors',
            'description',
            'start_date',
            'duration',
            'count_lessons',
        )
