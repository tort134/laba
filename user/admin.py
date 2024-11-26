from django.contrib import admin
from .models import Survey, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1

class SurveyAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]

admin.site.register(Survey, SurveyAdmin)
admin.site.register(Choice)