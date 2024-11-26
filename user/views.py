from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.views.generic import ListView, DetailView

from .models import Survey, Choice

def user_login(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                form.add_error(None, 'Неверное имя пользователя или пароль')
    else:
        form = LoginForm()

    return render(request, 'user/login.html', {'form': form})

def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            messages.success(request, 'Вы успешно зарегистрированы! Теперь вы можете войти')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'user/register.html', {'form': form})


def profile(request):
    status = request.GET.get('status')
    return render(request, 'user/profile.html', {
        'selected_status': status
    })

def survey_list(request):
    surveys = Survey.objects.all()
    return render(request, 'survey_list.html', {'surveys': surveys})

def vote(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id)
    try:
        selected_choice = survey.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'survey_detail.html', {
            'survey': survey,
            'error_message': 'Please select a choice.',
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return redirect('survey_results', survey_id=survey.id)