from django.urls import path
from . import views

app_name = 'indicators'

urlpatterns = [
    path('monthly-data/', views.monthly_data_entry, name='monthly_data'),
    path('dashboard/', views.admin_dashboard, name='dashboard'),
]
