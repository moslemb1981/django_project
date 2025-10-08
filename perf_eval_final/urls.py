from django.contrib import admin
from django.urls import path, include
from evaluations import views as eval_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', eval_views.dashboard, name='dashboard'),
    path('evaluations/', include('evaluations.urls')),
    path('users/', include('users.urls')),
    path('indicators/', include('indicators.urls')),
]
