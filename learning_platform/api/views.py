import django.db
from django.db.models import ObjectDoesNotExist
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer, AdminRenderer
from auth_app.models import User
from learning.models import Course
from .serializers import CourseSerializer, AnalyticCourseSerializer, AnalyticSerializer, UserSerializer
from .analytics import AnalyticReport


class CourseAPIView(APIView):
    http_method_names = ['get', 'options', ]
    parser_class = (JSONParser, MultiPartParser, FormParser, )
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer, AdminRenderer, )

    def get(self, request):
        courses_objects = Course.objects.all()
        courses_serializer = CourseSerializer(instance=courses_objects, many=True)
        return Response(data=courses_serializer.data, status=status.HTTP_200_OK)

    def get_view_name(self):
        return 'Список курсов'

    def get_view_description(self, html=False):
        return 'Информация о всех курсах, размещённых на платформе'


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








