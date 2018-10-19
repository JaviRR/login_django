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
            errors['email'] = "Email should be informed"
        elif not(EMAIL_REGEX.match(form['email'])):
            errors['email'] = "Email: Invalid email format."
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

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    objects = Validation()
