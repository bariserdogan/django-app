from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import RegisterForms, LoginForm

from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User

from django.contrib import messages
# Create your views here.


def register(request):
    form = RegisterForms(request.POST or None)  # Method'un post mu, get mi olduğunu kontrol etmemize gerek kalmıyor 
    if form.is_valid():
        username = form.cleaned_data.get("username") 
        password = form.cleaned_data.get("password") 

        newUser = User(username=username)
        newUser.set_password(password)
        newUser.is_superuser = True
        newUser.is_staff = True
        newUser.save()

        login(request) # redirection to login after registration
        
        messages.success(request,"Başarıyla kayıt oldunuz")
        
        return redirect("index")
    
    context = { 
        "form": form 
        }
    return render(request, "register.html", context)
        

def login(request):
    form = LoginForm(request.POST or None)
    context = { 
    "form": form 
    }
    if form.is_valid():
        username = form.cleaned_data.get("username") 
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if user is None:
            messages.warning(request,"Kullanıcı adı veya parola hatalı")
            return render(request, "login.html", context)
        messages.success(request, "Başarıyla giriş yaptınız. Hoşgeldiniz")
        auth_login(request, user) # sayfa ile aynı isimde olduğu için login'i as auth_login olarak aldık
        return redirect("index")
    else:
        return render(request,"login.html",context)

def logoutUser(request):
    
    logout(request)
    messages.success(request,"Başarıyla çıkış yaptınız.")
    return redirect("index")