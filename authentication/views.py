from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.


def loginView(request):
    template_name = 'authentication/login.html'
    if request.user.is_authenticated:
        return redirect('index')
    if request.method=="GET":
        return render(request,template_name)
    else:
        get_data=request.POST
        user = authenticate( username=get_data['username'], password=get_data['password'])
        if user is None:
            messages.info(request,'Wrong Credentials')
            return render(request,template_name)
        else:
            login(request,user)
            return redirect('index')
def logoutView(request):
    pass

def registerView(request):
    template_name = 'authentication/signup.html'
    if request.user.is_authenticated:
        return redirect('index')
    if request.method=="GET":
        return render(request,template_name)
    else:
        get_data=request.POST
        items = [get_data['username']]
        usererror=User.objects.filter(username__icontains=get_data['username']).first()
        if usererror:
            messages.info(request,'This username is unavailable.')
            return render(request,template_name)
        emailerror=User.objects.filter(email__icontains=get_data['email']).first()
        if emailerror:
            messages.info(request,'This email is already used.')
            return render(request,template_name)
        if get_data["password"]!=get_data["password2"]:
            messages.info(request,'Passwords didnt Match.')
            return render(request,template_name)
        newuser = User(username=get_data['username'],email=get_data['email'])
        newuser.set_password(get_data['password'])
        newuser.save()
        user = authenticate(username=get_data['username'],password=get_data['password'])
        login(request,user)
        return redirect('index')
