from django.shortcuts import render, HttpResponse, redirect
from apps.login.models import User
from django.contrib import messages
import bcrypt

def index(request):
    return render(request,"login/index.html")

def process_registration(request):
    errors = User.objects.validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request,value,extra_tags=key)
        return redirect('/')
    else:
        pwd = bcrypt.hashpw(request.POST['password1'].encode(), bcrypt.gensalt())
        User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = pwd
            )
        id = User.objects.last().id
        request.session['id'] = id
        messages.success(request, "Successfully registered (or logged in)!")
        return redirect('/success')

def success(request):
    if ("id" in request.session):
        context = {
            "name": User.objects.get(id = request.session['id']).first_name
        }
        return render(request,"login/success.html",context)
    else:
        return redirect('/')

def process_login(request):
    errors = User.objects.login_validator(request.POST)
    if (len(errors)):
        for key, value in errors.items():
            messages.error(request,value, extra_tags=key)
        return redirect('/')
    else:
        id = User.objects.get(email = request.POST['email']).id
        request.session['id'] = id
        messages.success(request, "Successfully registered (or logged in)!")
        return redirect('/success')