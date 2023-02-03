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


class CourseCreateView(CreateView):
    template_name = 'create.html'
    # Model of course to create
    model = Course
    form_class = CourseForm

    def get_success_url(self):
        return reverse('detail', kwargs={'course_id': self.object.id})

    def form_valid(self, form):
        # Get object with data from form but not save in database
        course = form.save(commit=False)
        course.author = self.request.user
        course.save()
        # Return after handle in parent class method "form_valid"
        return super(CourseCreateView, self).form_valid(form)


def delete(request, course_id):
    Course.objects.get(id=course_id).delete()
    return redirect('index')


class CourseDetailView(DetailView):
    template_name = 'detail.html'
    context_object_name = 'course'
    # Redefine name of default url parameter "pk" to "course_id"
    pk_url_kwarg = 'course_id'

    def get_queryset(self):
        return Course.objects.filter(id=self.kwargs.get('course_id'))

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        context['lessons'] = Lesson.objects.filter(course=self.kwargs.get('course_id'))
        return context


class CourseUpdateView(UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'create.html'
    # Redefine name of default url parameter "pk" to "course_id"
    pk_url_kwarg = 'course_id'

    # Method to get updated Course data
    def get_queryset(self):
        return Course.objects.filter(id=self.kwargs.get('course_id'))

    def get_success_url(self):
        return reverse('detail', kwargs={'course_id': self.object.id})


class CourseDeleteView(DeleteView):
    model = Course
    template_name = 'delete.html'
    # Redefine name of default url parameter "pk" to "course_id"
    pk_url_kwarg = 'course_id'

    # Method to get updated Course data
    def get_queryset(self):
        return Course.objects.filter(id=self.kwargs.get('course_id'))

    def get_success_url(self):
        return reverse('index')


def enroll(request, course_id):
    if request.user.is_anonymous:
        return redirect('login')
    else:
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
