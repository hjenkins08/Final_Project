from django.shortcuts import render, redirect
from .models import * 
from django.contrib import messages

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.validate(request.POST)
    if errors:
        for error in errors.values():
            messages.error(request, error)
        return redirect('/')
    else:
        new_user = User.objects.register(request.POST)
        request.session['user_id'] = new_user.id
        messages.success(request, "You have successfully registered!")
        return redirect('/success')

def login(request):
    if request.method == "GET":
        return redirect('/')
    if not User.objects.authenticate(request.POST['email'], request.POST['password']):
        messages.error(request, "Invalid Email/Password")
        return redirect('/')
    user = User.objects.get(email=request.POST['email'])
    request.session['user_id'] = user.id
    messages.success(request,"You have successfully logged in!")
    return redirect('/success')

def logout(request):
    request.session.clear()
    return redirect('/')

def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user,
        'wall_messages': Wall_Message.objects.all(),
        'books_listed' : Books_Listed.objects.all()
    }
    return render(request, 'success.html', context)

def post_message(request):
    Wall_Message.objects.create(message=request.POST['message'], poster=User.objects.get(id=request.session['user_id']))
    return redirect('/success')

def post_comment(request,id):
    poster = User.objects.get(id=request.session['user_id'])
    message = Wall_Message.objects.get(id=id)
    Comment.objects.create(comment=request.POST['comment'], poster=poster, wall_message=message)
    return redirect('/success')

def profile(request, id):
    context = {
        'user': User.objects.get(id=id)
    }
    return render(request, 'profile.html', context)

def add_like(request, id):
    liked_message = Wall_Message.objects.get(id=id)
    user_liking = User.objects.get(id=request.session['user_id'])
    liked_message.user_likes.add(user_liking)
    return redirect('/success')

def delete_comment(request, id):
    to_delete = Comment.objects.get(id=id)
    to_delete.delete()
    return redirect('/success')

def edit(request, id):
    # user = User.objects.get(id=id)
    comment = Comment.objects.get(id=id)
    context = {
        'user': User.objects.all(),
        'comment': comment
    }
    return render(request, "edit.html", context)

def update(request, id):
    to_edit = Comment.objects.get(id=id)
    to_edit.comment = request.POST['comment']
    to_edit.save()
    return redirect('/success')

def wants(request,id):
    wanted_book = Books_Listed.objects.get(id=id)
    user_wanting = User.objects.get(id=request.session['user_id'])
    wanted_book.user_wants.add(user_wanting)

    return redirect('/success')