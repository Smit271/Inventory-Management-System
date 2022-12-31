from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
from django.contrib.auth import login



def login_view(request):
    if request.method == 'GET':
        return render(request, 'authentication/login.html')
    else:
        user_obj = User.objects.filter(
            email=request.POST['email']
        ).first()

        if not user_obj:
            messages.warning(request, message="Email is not registered.")
            return render(request, 'authentication/login.html')
        else:
            if user_obj.check_password(request.POST['password']):
                login(request, user_obj)
                return redirect('products/home')
            else:
                messages.warning(request, message="Wrong credentials.")
                return render(request, 'authentication/login.html')

