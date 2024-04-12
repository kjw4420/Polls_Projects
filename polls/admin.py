from django.contrib import admin
from .models import *


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3 # 추가 옵션 창

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('질문 섹션', {'fields': ['question_text']}),
        ('생성일', {'fields':['pub_data'], 'classes': ['collapse']}),
    ]
    list_display = ('question_text','pub_data', 'was_published_recently')
    readonly_fields = ['pub_data']
    inlines = [ChoiceInline]
    list_filter = ['pub_data']
    search_fields = ['question_text', 'choice__choice_text']
    
admin.site.register(Question, QuestionAdmin)