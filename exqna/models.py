# exqna/models.py
from django.db import models
from django.conf import settings

class ExtraQuestion(models.Model):
    # 추가 질문
    title = models.CharField(max_length=32, null=False, verbose_name='제목') # 제목
    questioned_at = models.DateTimeField(verbose_name='질문일') # 질문 날짜

    def __str__(self):
        return self.title


class ExtraAnswer(models.Model):
    #추가 질문에 대한 답변
    user = models.ForeignKey(settings.AUTH_USER_MODEL) # 유저와 1:N 관계 설정
    question = models.ForeignKey(ExtraQuestion) # 질문 모델과 1:N 관계 설정
    content = models.TextField(max_length=256, blank=True) # 답변 내용
    is_public = models.BooleanField(default=False) # 공개/비공개
    created_at = models.DateTimeField(auto_now_add=True) # 생성 날짜
    updated_at = models.DateTimeField(auto_now=True) # 수정 날짜

    def __str__(self):
        return '{}에 대한 {}의 답변{}'.format(self.question, self.user, self.content)

class Requied(models.Model):
    #요청 질문과 그 내용
    user = models.ForeignKey(settings.AUTH_USER_MODEL) # 유저와 1:N 관계 설정
    title = models.CharField(max_length=32, null=False, verbose_name='요청 질문') # 요청 질문
    content = models.TextField(max_length=256) # 그에 대한 자신의 답변 내용
    created_at = models.DateTimeField(auto_now_add=True) # 생성 날짜
    updated_at = models.DateTimeField(auto_now=True) # 수정 날짜

    def __str__(self):
        return '{}의 요청 질문: {}'.format(self.user, self.title)