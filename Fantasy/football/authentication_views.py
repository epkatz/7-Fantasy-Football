from Fantasy.football.models import Team
from Fantasy.football.user_contact import registration_email
from Fantasy.football.views import add_message_all
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import render_to_response, redirect

def login_page(request):
    return render_to_response('index.html', {'template_name' : 'forms/login.html'})

def do_login(request):
    if request.user.is_authenticated():
            return redirect('/')
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
    #Could do better error messages (ie. you didn't put a username, wrong password, username dne)
    return render_to_response('index.html', {'template_name' : 'forms/login.html', 'error_message' : 'Username or Password was incorrect'})

def do_logout(request):
    logout(request)
    return render_to_response('index.html', {'template_name' : 'forms/login.html'})

def do_register(request):
    if request.method == 'POST':
        username=request.POST['username']
        if User.objects.filter(username__exact=username):
            return render_to_response('index.html', {'template_name' : 'forms/login.html', 'error_message' : 'The username is already taken'})
        email=request.POST['email']
        try:
            validate_email(email)
        except ValidationError:
            return render_to_response('index.html', {'template_name' : 'forms/login.html', 'error_message' : 'Not a valid email'})
        password1=request.POST['password1']
        password2=request.POST['password2']
        team_name=request.POST['team_name']
        if password1 != password2:
            return render_to_response('index.html', {'template_name' : 'forms/login.html', 'error_message' : 'Passwords do not match'})
        User.objects.create_user(username, email, password1)
        user = authenticate(username=username, password=password1)
        if user is not None:
            new_team = Team(team_name=team_name, owner=user)
            new_team.save()
            registration_email(username, email, team_name)
            login(request, user)
            add_message_all(username + " joined your league!")
            return redirect('/')
    return render_to_response('index.html', {'template_name' : 'forms/login.html', 'error_message' : 'Could not register new user'})

def change_password(request):
    return render_to_response('index.html', {'template_name' : 'forms/change_password.html'}) 

#Assumed the user is logged in, otherwise will redirect to LOGIN_URL defined in settings
@login_required
def do_change_password(request):
    if request.method == 'POST':
        old_pass=request.POST['old_pass']
        new_pass1=request.POST['new_pass1']
        new_pass2=request.POST['new_pass2']
        if not request.user.check_password(old_pass):
            return render_to_response('index.html', {'template_name' : 'forms/login.html', 'error_message' : 'Incorrect password'})
        if new_pass1 != new_pass2:
            return render_to_response('index.html', {'template_name' : 'forms/login.html', 'error_message' : 'Passwords don\'t match'})
        request.user.set_password(new_pass1)
        request.user.save()
        return redirect('/')
    return render_to_response('index.html', {'template_name' : 'forms/login.html', 'error_message' : 'Page is no longer available'})

