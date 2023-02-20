from .models import Course, Review, Lesson
from django import forms
from django.forms.widgets import Textarea, TextInput
from django.core.exceptions import ValidationError


class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = ('title', 'description', 'start_date', 'duration', 'price', 'count_lessons',)


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ('content', )


class LessonForm(forms.ModelForm):
    # course = forms.ModelChoiceField(label='Курс')
    # course = forms.ModelChoiceField(queryset=Course.objects.all(), empty_label='Выберите курс', required=True,
    #                                 label='Kурс', help_text='Укажите курс, к которому вы хотите добавить урок')
    preview = forms.CharField(widget=Textarea(attrs={
        'placeholder': 'Опишите содержание урока.',
        'rows': 20,
        'cols': 50,
    }), label='')

    class Meta:
        model = Lesson
        fields = ('name', 'preview', )
        labels = {'name': '', 'preview': '', }
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Введите название урока.'}),
            'preview': Textarea(attrs={
                                        'placeholder': 'Опишите содержание урока.',
                                        'rows': 20,
                                        'cols': 50,
            })
        }
        help_texts = {'preview': 'Описание не должно быть пустым'}

    def clean_preview(self):
        preview_data = self.cleaned_data['preview']
        if len(preview_data) > 200:
            raise ValidationError('Слишком длинное описание. Сократите его до 200 символов.')
        return preview_data
