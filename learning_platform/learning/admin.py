from django.contrib import admin
from .models import Course, Lesson, Review


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'description',)
    list_display_links = ('title', 'start_date', )
    list_editable = ('description', )
    list_per_page = 3
    search_fields = ('title', 'start_date', 'description', )
    actions_on_top = True
    actions_on_bottom = True
    actions_selection_counter = True
    save_on_top = True
    # To pretty display many to many fields of db
    filter_horizontal = ('authors', )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('course', 'name', 'preview', )
    search_fields = ('name', )
    list_per_page = 3
    actions_on_top = False
    actions_on_bottom = True
    actions_selection_counter = True


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', )
    search_fields = ('content', )
    list_per_page = 100
