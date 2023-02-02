from .models import Course
from django import forms


class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = ('title', 'description', 'start_date', 'duration', 'price', 'count_lessons',)
