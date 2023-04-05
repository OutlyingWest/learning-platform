from datetime import datetime

from django.db.models import Count, Sum
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField, StringRelatedField, Serializer
from learning.models import Course, Tracking
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


class AnalyticCourseSerializer(Serializer):
    date = serializers.SerializerMethodField()
    course = serializers.SerializerMethodField()
    views = serializers.SerializerMethodField()
    count_students = serializers.SerializerMethodField()
    percent_passed = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    # @staticmethod
    def get_course(self, instance) -> str:
        return instance.course.title

    def get_views(self, instance) -> int:
        request = self.context.get('request')
        views_dict = request.session.get('views', {})
        return views_dict.get(str(instance.course.id), 0)

    def get_url(self, instance) -> str:
        request = self.context.get('request')
        return f"{request.scheme}://{request.META['HTTP_HOST']}{{instance.course.get_absolute_url(}}"

    def get_count_students(self, instance) -> int:
        total_students = (
            Tracking.objects
            .filter(lesson__course=instance.course.id)
            .values('lesson__course')
            .aggregate(Count('user', distinct=True))
        )

        return total_students['user__count']

    def get_percent_passed(self, instance) -> float:
        course_id = instance.course.id

        students = Tracking.objects.filter(lesson__course=course_id).values('user').distinct()
        users_percent = list()
        for student_id in range(len(students)):
            percents = (
                Tracking.objects.
                filter(lesson__course=course_id, user=students[student_id]['user']).
                aggregate(total=Count('lesson'), fact=Sum('passed'))
            )
            user_percent = float(percents['fact'] / percents['total'] * 100)
            users_percent.append(user_percent)

        try:
            total_percent = round(sum(users_percent) / len(users_percent), 2)
            return total_percent
        except ZeroDivisionError:
            return 0

    def get_date(self, instance):
        return datetime.now()


