from django.shortcuts import render , redirect
from .forms import RegisterForm,LoginForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login , authenticate , logout

# Create your views here.

def loginUser(request):

    form=LoginForm(request.POST or None)

    context={
        "form":form
    }

    if form.is_valid():
        username=form.cleaned_data.get("username")
        password=form.cleaned_data.get("password")
        user = authenticate(username = username,password = password)

        if user is None:
            messages.info(request,"Kullanıcı Bulunamadı...")
            return render(request,"login.html",context)
        
        messages.success(request,"Başarıyla Giriş Yapıldı...")
        login(request,user)
        return redirect("index")
    return render(request,"login.html",context)

def logoutUser(request):
    logout(request)
    messages.success(request,"Çıkış Yapıldı")
    return redirect("index")

def register(request):

    form=RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        newUser=User(username=username)
        newUser.set_password=(password)

        newUser.save()
        login(request,newUser)
        messages.success(request,"Kayıt Yapıldı")
        
        return redirect("index")
    
    context = {
        "form" : form
    }
    return render(request,"register.html",context)
