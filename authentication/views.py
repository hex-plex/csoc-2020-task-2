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
    pass
