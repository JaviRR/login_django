from django.db import models
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

class Validation(models.Manager):
    def validator(self, form):
        errors = {}
        if (len(form['first_name']) < 2):
            errors['first_name'] = "First name should have at least two characters"
        elif not(NAME_REGEX.match(form['first_name'])):
            errors['first_name'] = "First name: Invalid format. Only alphabetic characters allowed"
        if (len(form['last_name']) < 2):
            errors['last_name'] = "Last Name should have at least two characters"
        elif not(NAME_REGEX.match(form['last_name'])):
            errors['last_name'] = "Last name: Invalid format. Only alphabetic characters allowed"
        if (len(form['email']) < 2):
            errors['email'] = "Email should be have at least 2 characters"
        elif not(EMAIL_REGEX.match(form['email'])):
            errors['email'] = "Email: Invalid email format."
        elif User.objects.filter(email = form['email']):
            errors['email'] = "Email already in use"
        if (len(form['password1']) < 1):
            errors['password'] = "Password should be informed"
        elif (form['password1'] != form['password2']):
            errors['password'] = "Password don't match"
        return errors
    def login_validator(self, form):
        errors = {}
        if (len(form['email']) < 1):
            errors['login'] = "Email should be informed"
        else:
            try:
                user = User.objects.get(email=form['email'])
            except:
                errors['login'] = "Email doesn't found in the database"
        if not(len(errors)):
            if not(bcrypt.checkpw(form['password'].encode(), user.password.encode())):
                errors['login'] = "Invalid credentials"
    
        return errors

    def quote_validator(self, form):
        errors = {}
        if (len(form['author']) < 4):
            errors['author'] = "Author should have more than 3 characters"
        if (len(form['quote']) < 11):
            errors['quote'] = "Quotes should have more than 10 characters"
        return errors

    def edit_validator(self, form):
        errors = {}
        if (len(form['first_name']) < 1):
            errors['first_name'] = "First Name should be informed"
        if (len(form['last_name']) < 1):
            errors['last_name'] = "Last Name should be informed"
        if not(EMAIL_REGEX.match(form['email'])):
            errors['email'] = "Email: Invalid email format."
        elif User.objects.filter(email = form['email']).exclude(id=form['id']):
            errors['email'] = "Email already in use"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    objects = Validation()

class Quote(models.Model):
    author = models.CharField(max_length=255)
    quote = models.TextField(max_length=1000)
    user = models.ForeignKey(User,related_name="quotes", on_delete=models.CASCADE)
    liked = models.ManyToManyField(User, related_name="like")
    objects = Validation()