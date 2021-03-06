from django.db import models
from django.conf import settings

class Question(models.Model):
    # 질문
    question = models.CharField(max_length=128, null=False) # 제목
    month = models.CharField(max_length=2, null=False)
    day = models.CharField(max_length=2, null=False)

    def __str__(self):
        return self.question

class Answer(models.Model):
    # 답변
    user = models.ForeignKey(settings.AUTH_USER_MODEL) # 유저와 1:N 관계 설정
    question = models.ForeignKey(Question) # 질문 모델과 1:N 관계 설정
    content = models.TextField(max_length=256) # 답변 내용
    is_public = models.BooleanField(default=False) # 공개/비공개
    created_at = models.DateTimeField(auto_now_add=True) # 생성 날짜
    updated_at = models.DateTimeField(auto_now=True) # 수정 날짜

    def __str__(self):
        return '{}에 대한 {}의 답변{}'.format(self.question, self.user, self.content)

