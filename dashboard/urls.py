from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='dashboard'),  # 🔹 اینجا نام را از 'home' به 'dashboard' تغییر دادیم
]
