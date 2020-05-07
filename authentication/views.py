from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
# Create your views here.


def loginView(request):
    template_name = 'authentication/login.html'
    if request.user.is_authenticated:
        return redirect('index')
    if request.method=="GET":
        return render(request,'login.html')
    else:
        get_data=request.POST
        user = authenticate(request, get_data['username'], get_data['password'])
        if user is None:
            return render(request,'login.html',{'message':'Wrong Credentials'})
        else:
            login(request,user)
            return redirect('index')
def logoutView(request):
    pass

def registerView(request):
    pass
