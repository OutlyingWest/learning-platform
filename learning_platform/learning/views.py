from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import NON_FIELD_ERRORS
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
from datetime import datetime
from django import forms
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from .models import Course, Lesson, Tracking, Review
from .forms import CourseForm, ReviewForm, LessonForm, OrderByAndSearchForm, SettingsForm


class MainView(ListView, FormView):
    template_name = 'index.html'
    queryset = Course.objects.all()
    context_object_name = 'courses'

    form_class = OrderByAndSearchForm

    paginate_by = 6

    def get_queryset(self):
        queryset = MainView.queryset
        if {'search', 'price_order'} != self.request.GET.keys():
            return queryset
        else:
            search_query = self.request.GET.get('search')
            price_order_by = self.request.GET.get('price_order')
            query_filter = Q(title__icontains=search_query) | Q(description__icontains=search_query)
            queryset = queryset.filter(query_filter).order_by(price_order_by)
            return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context['current_year'] = datetime.now().year
        return context

    def get_initial(self):
        """ For don't forget search forms fields """
        initial = super(MainView, self).get_initial()
        initial['search'] = self.request.GET.get('search', '')
        initial['price_order'] = self.request.GET.get('price_order', 'title')
        return initial

    def get_paginate_by(self, queryset):
        """
        After implementation of this method "page_obj"
        variable will be added to index.html template
        """
        return self.request.COOKIES.get('paginate_by', settings.DEFAULT_COURSES_ON_PAGE)


class CourseCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'create.html'
    # Model of course to create
    model = Course
    form_class = CourseForm

    permission_required = ('learning.add_course', )

    def get_success_url(self):
        return reverse('detail', kwargs={'course_id': self.object.id})

    def form_valid(self, form):
        with transaction.atomic():
            # Get object with data from form but not save in database
            course = form.save(commit=False)
            course.author = self.request.user
            course.save()
            # Return after handle in parent class method "form_valid"
            return super(CourseCreateView, self).form_valid(form)


class CourseDetailView(ListView):
    template_name = 'detail.html'
    # Contains value from get_queryset()
    context_object_name = 'lessons'
    # Redefine name of default url parameter "pk" to "course_id"
    pk_url_kwarg = 'course_id'

    def get(self, request, *args, **kwargs):
        """ Allows to get data about page views """
        views: dict = request.session.setdefault('views', {})
        course_id = str(kwargs[CourseDetailView.pk_url_kwarg])
        count = views.get(course_id, 0)
        views[course_id] = count + 1
        request.session['views'] = views
        # Send cookies in every request
        request.session.modified = True
        return super(CourseDetailView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return Lesson.objects.select_related('course').filter(course=self.kwargs.get(self.pk_url_kwarg))

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        context['reviews'] = Review.objects.select_related('user').filter(course=self.kwargs.get(self.pk_url_kwarg))
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


@transaction.atomic
# This decorator check is user authenticate, else redirect to LOGIN_URL
@login_required
# Permissions can be checked in "auth_permission" table in database
@permission_required('learning.add_tracking', raise_exception=True)
def enroll(request, course_id):
    is_existed = Tracking.objects.filter(user=request.user).exists()
    if is_existed:
        return HttpResponse('???? ?????? ???????????????? ???? ???????????? ????????')
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
        return HttpResponse('???? ???????????????? ???? ???????????? ????????')


class LessonCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Lesson
    form_class = LessonForm
    template_name = 'create_lesson.html'
    pk_url_kwarg = 'course_id'

    permission_required = ('learning.add_lesson', )

    def get_form(self, form_class=None):
        form = super(LessonCreateView, self).get_form()
        course_queryset = Course.objects.filter(authors=self.request.user)
        form.fields['course'] = forms.ModelChoiceField(queryset=course_queryset, label='????????',
                                                       initial={'title': course_queryset[0].title})
        return form

    def get_success_url(self):
        return reverse('detail', kwargs={self.pk_url_kwarg: self.kwargs.get(self.pk_url_kwarg)})


@transaction.non_atomic_requests
@login_required
@permission_required('learning.add_review', raise_exception=True)
def review(request, course_id):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.errors:
            errors = form.errors[NON_FIELD_ERRORS]
            return render(request, 'review.html', {'form': form, 'errors': errors})
        if form.is_valid():
            # cleaned_data contains all form fields if form is valid
            data = form.cleaned_data
            Review.objects.create(content=data['content'],
                                  course=Course.objects.get(id=course_id),
                                  user=request.user)
        return redirect(reverse('detail', kwargs={'course_id': course_id}))
    else:
        form = ReviewForm()
        return render(request, 'review.html', {'form': form})


def add_course_to_favorites(request, course_id):
    if request.method == 'POST':
        favorites: list = request.session.get('favorites', list())
        favorites.append(course_id)
        request.session['favorites'] = favorites
        request.session.modified = True
    return redirect(reverse('index'))


def remove_course_from_favorites(request, course_id):
    if request.method == 'POST':
        request.session.get('favorites').remove(course_id)
        request.session.modified = True
    return redirect(reverse('index'))


class FavoriteCoursesView(MainView):
    """ Class allow to view and search only favorite courses """
    def get_queryset(self):
        queryset = super(FavoriteCoursesView, self).get_queryset()
        favorites_ids = self.request.session.get('favorites', list())
        return queryset.filter(id__in=favorites_ids)


class SettingsFormView(FormView):
    form_class = SettingsForm
    template_name = 'settings.html'

    def post(self, request, *args, **kwargs):
        paginate_by = request.POST.get('paginate_by')
        cookies_max_age = settings.COOKIES_REMEMBER_AGE
        # Allow to redirect after cookie set
        response = HttpResponseRedirect(reverse('index'), '?????????????????? ?????????????? ??????????????????!')
        response.set_cookie('paginate_by', value=paginate_by, secure=False, httponly=False,
                            samesite='Lax', max_age=cookies_max_age)
        return response

    def get_initial(self):
        """ For display previously set settings """
        initial = super(SettingsFormView, self).get_initial()
        initial['paginate_by'] = self.request.COOKIES.get('paginate_by', settings.DEFAULT_COURSES_ON_PAGE)
        return initial
