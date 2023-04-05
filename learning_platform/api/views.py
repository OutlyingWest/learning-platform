from django.db.models import ObjectDoesNotExist
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from auth_app.models import User
from learning.models import Course
from .serializers import CourseSerializer, AnalyticCourseSerializer, AnalyticSerializer
from .analytics import AnalyticReport


@api_view(['GET', 'POST'])
def courses(request):
    courses_objects = Course.objects.all()
    courses_serializer = CourseSerializer(instance=courses_objects, many=True)
    return Response(data=courses_serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def courses_id(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
        course_serializer = CourseSerializer(instance=course, many=False)
        return Response(data=course_serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist as exception:
        return Response(data={'error': 'Запрашиваемый курс отсутствует в системе'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def analytics(request):
    courses_objects = Course.objects.all()
    reports = [AnalyticReport(course=course) for course in courses_objects]
    analytic_serializer = AnalyticSerializer(reports, many=False, context={'request': request})
    return Response(data=analytic_serializer.data, status=status.HTTP_200_OK)






