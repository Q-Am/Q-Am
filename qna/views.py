# qna/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Question, Answer
# import time
from .forms import AnswerForm


def question(request,user_id):
    #days=time.strftime('%j', time.localtime(time.time()))
    days='1'
    #days에 걸리는 함수를 통해 오늘이 365일 중에 몇 번째 날인지 파악
    now=int(days)
    ques=Question.objects.get(id=now)
    #그날에 맞는 질문을 골라 온다.

    if request.method=='POST':
        form=AnswerForm(request.POST,request.FILES)
        if form.is_valid():
            answer=form.save(commit=False)
            answer.user_id = user_id
            answer.question = ques
            answer.save()
            return redirect('exqna:exquestion', user_id=user_id)
    else :
        form = AnswerForm()
    return render(request, 'qna/question.html', {
            'form':form,
            'question' : ques,
        })

def main(request):
    return render(request, 'qna/main.html')

def question_edit(request, answer_id):
    #days=time.strftime('%j', time.localtime(time.time()))
    days='1'
    #days에 걸리는 함수를 통해 오늘이 365일 중에 몇 번째 날인지 파악
    now=int(days)
    ques=Question.objects.get(id=now)
    #그날에 맞는 질문을 골라 온다.
    answer=get_object_or_404(Answer,id=answer_id)
    if request.method=='POST':
        form=AnswerForm(request.POST,request.FILES,instance=answer)
        if form.is_valid():
            new_answer = form.save(commit=False)
            new_answer.user_id = answer.user_id
            new_answer.question = answer.question
            new_answer.save()
            return redirect('qna:main')
    else :
        form = AnswerForm(instance=answer)
    return render(request, 'qna/question_edit.html', {
            'form':form,
            'question' : ques,
        })

