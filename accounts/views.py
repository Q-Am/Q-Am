from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login as auth_login
from .forms import SignupForm, ProfileForm,EditPasswordForm
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.templatetags.socialaccount import get_providers
from accounts.models import Profile
from django.core.urlresolvers import reverse
from django.contrib.auth.views import password_reset, password_reset_confirm
from django.contrib.auth import get_user_model
from django.contrib import messages


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()

            return redirect(settings.LOGIN_URL)  # default : '/accounts/login'
    else:
        form = SignupForm()

    return render(request, 'accounts/signup_form.html', {'form': form, })



@login_required
def signup_info(request):
    #회원 가입 추가정보 받아오기
    if Profile.objects.filter(user=request.user).exists():
        # 프로필이 이미 있으면 질문페이지로
        return redirect('qna:main')
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()

            return redirect('qna:question')
    else:
        form = ProfileForm

    return render(request, 'accounts/signup_info.html', {
        'form': form,
        })




@login_required
def signup_info(request):
    # 회원 가입 추가정보 받아오기
    if Profile.objects.filter(user=request.user).exists():
        # 프로필이 이미 있으면 질문페이지로
        return redirect('qna:question')

    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            try:
                # 카카오가 있으면
                profile.user.username = profile.user.socialaccount_set.first().extra_data['properties']['nickname'] # 유저의 이름은 카카오톡 닉네임으로 저장
            except AttributeError:
                # 없어서 에러가 나면
                profile.user.username = profile.nickname
            finally:
                profile.user.save()
                profile.save()

            return redirect('qna:question')
    else:
        form = ProfileForm()

    return render(request, 'accounts/signup_info.html', {
        'form': form,
        })


@login_required
def profile(request):
    return render(request, 'accounts/profile.html')



def login(request):
    providers = []
    for provider in get_providers():

        # social_app속성은 provider에는 없는 속성입니다.
        try:
            provider.social_app = SocialApp.objects.get(provider=provider.id, sites=settings.SITE_ID)

        except SocialApp.DoesNotExist:
            provider.social_app = None
        providers.append(provider)

    return auth_login(request,
                      template_name='accounts/login_form.html',
                      extra_context={'providers': providers})


@login_required
def edit_pw(request):
    user = get_user_model()
    user = user.objects.get(username=request.user)


    if request.method == 'POST':
        pw1 = request.POST.get('pw1')
        pw2 = request.POST.get('pw2')
        if pw1 != pw2 :
            messages.info(request, '새로운 비밀번호 두개가 일치하지 않습니다.')
            return redirect('accounts:edit_pw')
        else:
            user.set_password(pw1)
            user.save()
        return redirect('accounts:login')
    else:
        form = EditPasswordForm

        return render(request, 'accounts/edit_pw.html', {
            'form': form
        })

#비밀번호 찾기
def reset(request):
    return password_reset(request,
        template_name='accounts/reset.html',
        email_template_name='accounts/reset_email.html',
        subject_template_name='accounts/reset_subject.txt',
        post_reset_redirect=reverse('accounts:login'))


def reset_confirm(request, uidb36=None, token=None):
    return password_reset_confirm(request, template_name='accounts/reset_confirm.html',
        uidb36=uidb36, token=token, post_reset_redirect=reverse('accounts:login'))


