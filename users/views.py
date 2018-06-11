from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpRequest, JsonResponse
from django.urls import reverse
from django.contrib.auth.models import User

from .forms import LoginForm, RegistrationForm


def log_in(request):
    form = LoginForm(request.POST)

    if form.is_valid():
        username = form.cleaned_data['login_username']
        password = form.cleaned_data['login_password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            response = {
                'has_error': False
            }
        else:
            response = {
                'has_error': True,
                'error_msg': "Request failed, please retry."
            }

        return JsonResponse(response)


def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


def registration(request):
    form = RegistrationForm(request.POST)

    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        email = form.cleaned_data['email']
        firstname = form.cleaned_data['firstname']
        lastname = form.cleaned_data['lastname']

        if email == "":
            email = "default@default.com"

        try:
            user = User.objects.create_user(username, email, password)
        except Exception:
            response = {
                'has_error': True,
                'error_msg': "Request failed, please retry."
            }
        else:
            user.first_name = firstname
            user.last_name = lastname
            user.save()

            response = {
                'has_error': False
            }

    else:
        response = {
            'has_error': True,
            'error_msg': "Passwords don't match!"
        }

    return JsonResponse(response)


def registration_success(request):
    return render(request, 'users/registration_success.html')
