import django.db
from django.db.models import ObjectDoesNotExist
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status, serializers
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer, AdminRenderer
from auth_app.models import User
from learning.models import Course
from .serializers import CourseSerializer, AnalyticCourseSerializer, AnalyticSerializer, UserSerializer
from .analytics import AnalyticReport


class CourseListAPIView(ListAPIView):
    """Полный список курсов, размещённых на платформе"""
    name = 'Список курсов'
    serializer_class = CourseSerializer
    authentication_classes = (TokenAuthentication, )
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter, )
    search_fields = ('title', 'description', 'authors__first_name', 'authors__last_name', )
    ordering_fields = ('start_date', 'price', )
    ordering = 'title'

    def get_queryset(self):
        return Course.objects.all()


class CourseRetrieveAPIView(RetrieveAPIView):
    """Получение курса по id, переданному в URL"""
    name = 'Курс'
    serializer_class = CourseSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'course_id'

    def get_queryset(self):
        return Course.objects.all()


@api_view(['GET'])
def analytics(request):
    courses_objects = Course.objects.all()
    reports = [AnalyticReport(course=course) for course in courses_objects]
    analytic_serializer = AnalyticSerializer(reports, many=False, context={'request': request})
    return Response(data=analytic_serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def users(request):
    if request.method == 'GET':
        users_objects = User.objects.all()
        user_serializer = UserSerializer(instance=users_objects, many=True)
        return Response(data=user_serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        user_serializer = UserSerializer(data=request.data)
        try:
            if user_serializer.is_valid(raise_exception=True):
                user_serializer.instance = user_serializer.save(user_serializer.validated_data)
                return Response(data=user_serializer.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError:
            return Response(data=user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except django.db.IntegrityError:
            return Response(data={'email': 'Пользователь с таким email ужe существует'},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as exception:
            return Response(data={'error': str(exception)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
