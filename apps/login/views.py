from django.shortcuts import render, HttpResponse, redirect
from apps.login.models import User, Quote
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
        return redirect("/quotes")

def process_login(request):
    errors = User.objects.login_validator(request.POST)
    if (len(errors)):
        for key, value in errors.items():
            messages.error(request,value, extra_tags=key)
        return redirect('/')
    else:
        id = User.objects.get(email = request.POST['email']).id
        request.session['id'] = id
        return redirect("/quotes")

def quotes(request):
    if "id" in request.session:
        context = {
            "user": User.objects.get(id = request.session['id']),
            "quotes": Quote.objects.all()
        }
        return render(request, "login/quotes.html", context)
    else:
        return redirect("/")

def process_quote(request):
    if "id" in request.session:
        errors = User.objects.quote_validator(request.POST)
        if (len(errors)):
            for key, value in errors.items():
                messages.error(request,value,extra_tags=key)
            return redirect("/quotes")
        else:
            Quote.objects.create(
                author = request.POST['author'],
                quote = request.POST['quote'],
                user = User.objects.get(id = request.session['id'])
            )
            return redirect("/quotes")
    else:
        return redirect("/")

def edit(request, id):
    if "id" in request.session:
        context = {
            "user": User.objects.get(id = request.session['id'])
        }
        return render(request, "login/edit.html", context)
    else:
        return redirect("/")

def process_edit(request):
    if "id" in request.session:
        errors = User.objects.edit_validator(request.POST)
        if (len(errors)):
            for key, value in errors.items():
                messages.error(request,value,extra_tags=key)
            return redirect("/myaccount/"+str(request.session['id']))
        else:
            user = User.objects.get(id = request.session['id'])
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            user.save()
            return redirect("/quotes")
    else:
        return redirect("/")

def like(request):
    if "id" in request.session:
        quote = Quote.objects.get(id=request.POST['like'])
        quote.liked.add(User.objects.get(id = request.POST['liked']))
        quote.save()
        return redirect("/quotes")
    else:
        return redirect("/")

def delete_quote(request, id):
    if "id" in request.session:
        Quote.objects.get(id = id).delete()
        return redirect("/quotes")
    else:
        return redirect("/")

def profile(request, id):
    if "id" in request.session:
        context = {
            "user": User.objects.get(id = id),
            "quotes": Quote.objects.filter(user = User.objects.get(id = id))
        }
        return render(request, "login/profile.html", context)
    else:
        return redirect("/")

def logout(request):
    request.session.clear
    return redirect("/")