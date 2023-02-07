from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from datetime import datetime
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Course, Lesson, Tracking
from .forms import CourseForm


class MainView(ListView):
    template_name = 'index.html'
    queryset = Course.objects.all()
    context_object_name = 'courses'

    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context['current_year'] = datetime.now().year
        return context


class CourseCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'create.html'
    # Model of course to create
    model = Course
    form_class = CourseForm

    permission_required = ('learning.add_course', )

    def get_success_url(self):
        return reverse('detail', kwargs={'course_id': self.object.id})

    def form_valid(self, form):
        # Get object with data from form but not save in database
        course = form.save(commit=False)
        course.author = self.request.user
        course.save()
        # Return after handle in parent class method "form_valid"
        return super(CourseCreateView, self).form_valid(form)


class CourseDetailView(DetailView):
    template_name = 'detail.html'
    context_object_name = 'course'
    # Redefine name of default url parameter "pk" to "course_id"
    pk_url_kwarg = 'course_id'

    def get_queryset(self):
        return Course.objects.filter(id=self.kwargs.get(self.pk_url_kwarg))

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        context['lessons'] = Lesson.objects.filter(id=self.kwargs.get(self.pk_url_kwarg))
        return context


class CourseUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'create.html'
    # Redefine name of default url parameter "pk" to "course_id"
    pk_url_kwarg = 'course_id'

    permission_required = ('learning.change_course', )

    # Method to get updated Course data
    def get_queryset(self):
        return Course.objects.filter(id=self.kwargs.get(self.pk_url_kwarg))

    def get_success_url(self):
        return reverse('detail', kwargs={self.pk_url_kwarg: self.object.id})


class CourseDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Course
    template_name = 'delete.html'
    # Redefine name of default url parameter "pk" to "course_id"
    pk_url_kwarg = 'course_id'

    permission_required = ('learning.delete_course', )

    # Method to get updated Course data
    def get_queryset(self):
        return Course.objects.filter(id=self.kwargs.get(self.pk_url_kwarg))

    def get_success_url(self):
        return reverse('index')


# This decorator check is user authenticate, else redirect to LOGIN_URL
@login_required
# Permissions can be checked in "auth_permission" table in database
@permission_required('learning.add_tracking', raise_exception=True)
def enroll(request, course_id):
    is_existed = Tracking.objects.filter(user=request.user).exists()
    if is_existed:
        return HttpResponse('Вы уже записаны на данный курс')
    else:
        lessons = Lesson.objects.filter(course=course_id)
        records = [
            Tracking(
                lesson=lesson,
                user=request.user,
                passed=False
            ) for lesson in lessons
        ]
        Tracking.objects.bulk_create(records)
        return HttpResponse('Вы записаны на данный курс')
