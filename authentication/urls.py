from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginView, name="Login"),
    path('signup/', views.registerView, name="Signup"),
    path('logout/', views.logoutView, name="Logout")
]
