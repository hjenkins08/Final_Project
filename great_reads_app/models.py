from django.db import models
import re
import bcrypt 
from datetime import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validate(self, form):
        errors = {}
        if len(form['first_name']) < 2:
            errors['first_name'] = "First Name must be at least 2 characters"
        if len(form['last_name']) < 2:
            errors['last_name'] = "Last Name must be at least 2 characters"
        if not EMAIL_REGEX.match(form['email']):
            errors['email'] = "Invalid email address"
        email_check = self.filter(email=form['email'])
        if email_check:
            errors['email'] = "Email already in use"
        if len(form['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        if form['password'] != form['confirm']:
            errors['password'] = "Passwords do not match"
        return errors
    
    def authenticate(self, email, password):
        users = self.filter(email=email)
        if not users:
            return False

        user = users[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())
    
    def register (self, form):
        pw = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt()).decode()
        return self.create(
            first_name = form['first_name'],
            last_name = form['last_name'],
            email = form['email'],
            password = pw,
        )

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    birthday = models.DateField(null=True)
    #wants_posts

    objects = UserManager() 

    def __repr__(self):
        return f"<User.object:{self.first_name} {self.last_name} {self.email}>"

class Wall_Message(models.Model):
    message = models.CharField(max_length=255)
    poster = models.ForeignKey(User, related_name='user_messages', on_delete=models.CASCADE)
    user_likes = models.ManyToManyField(User, related_name='liked_posts')
    
class Books_Listed(models.Model):
    book_name = models.CharField(max_length=255, null=True)
    image_url = models.CharField(max_length=255, null=True)
    book_quote = models.TextField(null=True)
    user_wants = models.ManyToManyField(User, related_name='wants_posts')

    def __repr__(self):
        return f"<Post.object:{self.book_name}>"

class Comment(models.Model):
    comment = models.CharField(max_length=255)
    poster = models.ForeignKey(User, related_name='user_comments', on_delete=models.CASCADE)
    wall_message = models.ForeignKey(Wall_Message, related_name='post_comments', on_delete=models.CASCADE)

    def __repr__(self):
        return f"<Comment.object:{self.comment}>"