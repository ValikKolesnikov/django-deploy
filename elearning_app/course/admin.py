from django.contrib import admin
from .models import Course, Category, Lesson, Step, Theory, Test

admin.site.register(Course)
admin.site.register(Category)
admin.site.register(Lesson)
admin.site.register(Step)
admin.site.register(Theory)
admin.site.register(Test)
