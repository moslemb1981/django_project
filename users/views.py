from django.shortcuts import render
from .models import User
from django.contrib.auth.views import LoginView

def user_list(request):
    users = User.objects.all()
    return render(request, 'users/user_list.html', {'users': users})



class CustomLoginView(LoginView):
    template_name = 'users/login.html'
