from __future__ import unicode_literals
from django.db import models
import re, datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
class UserManager(models.Manager):
    def register_validator(self, postData):
        errors ={}
        last = postData['alias']

        if len(postData['name']) < 2 :
            errors['name'] = "Please enter a valid name."
        if len(postData['alias']) < 2 or not last.isalpha():
            errors['alias'] = "Please enter a valid alias name."
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Please enter a proper email."
        if len(postData['password']) < 7 :
            errors['password'] = "Please enter a better password."
        if postData['password']!=postData['cpassword']:
            errors['cpassword'] = "Password did not match. Please try again."
        return errors

    def login_validator(self, postData):
        errors ={}
        if not User.objects.filter(email=postData['loginemail']).exists():
            errors['logine'] = "Invalid email or password."
        if not EMAIL_REGEX.match(postData['loginemail']):
            errors['loginemail'] = "Please enter a proper email."
        if len(postData['loginpassword']) < 7 :
            errors['loginpassword'] = "Invalid info. Please try again."
        return errors

class BookManager(models.Manager):
    def book_validator(self, postData):
        errors ={}
        if len(postData['title']) < 1: 
            errors['title'] = "Please enter a title."
        if len(postData['new_author']) < 1:
            errors['new_author'] = "Please add an author."
        # date_from_form = postData['date']
        # if Book.created_at <=date_from_form:
        #     errors['date'] = "Please enter an older date!"
        if len(postData['date']) < 10:
            errors['datelen'] = "Please enter a valid date."
        if len(postData['review']) < 2:
            errors['review'] = "Please provide a review."
        return errors
    def review_validator(self, postData):
        errors ={}
        if len(postData['review']) < 2:
            errors['review'] = "Please provide a review."
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    alias= models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publish_date = models.DateField()
    creator = models.ForeignKey(User, related_name="books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()
    
class Review(models.Model):
    content = models.TextField(max_length=300)
    rating = models.IntegerField()
    reviewer = models.ForeignKey(User, related_name="reviews")
    books = models.ForeignKey(Book, related_name="has_reviews")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)







