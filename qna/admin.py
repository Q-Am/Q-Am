from django.contrib import admin
from .models import Question,Answer

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question','month','day']

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display=['user','question','content','is_public','created_at','updated_at']
