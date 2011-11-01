from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template.context import RequestContext

def home(request):
    if request.user.is_authenticated():
        return render_to_response('index.html', {'template_name' : 'home.html', 'username': request.user.username}, context_instance=RequestContext(request))
    else:
        return render_to_response('index.html', {'template_name' : 'forms/login.html'})
    
def add_message_all(message):
    users = User.objects.all()
    for user in users:
        user.message_set.create(message=message)