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
    preview = forms.CharField(widget=Textarea(attrs={
        'placeholder': 'Опишите содержание урока.',
        'rows': 20,
        'cols': 50,
    }), label='')

    error_css_class = 'error_field'
    required_css_class = 'required_field'

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


class OrderByAndSearchForm(forms.Form):
    """ Allow to search by price on main page """
    # For choices arg in ChoiceField()
    PRICE_CHOICES = (
        ('title', 'По умолчанию'),
        ('price', 'Caмые дешевые курсы'),
        ('-price', 'Caмые дорогие курсы'),
    )

    search = forms.CharField(label='Поиск', label_suffix=':', required=False,
                             widget=TextInput(attrs={'placeholder': 'Введите запрос'}))

    price_order = forms.ChoiceField(label='', choices=PRICE_CHOICES, initial=PRICE_CHOICES[0])
