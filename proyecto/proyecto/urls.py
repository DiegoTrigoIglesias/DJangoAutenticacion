from django.contrib import admin
from django.urls import path
from users import views

urlpatterns = [

    # Sección para usuarios
    path('', views.welcome),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('admin/', admin.site.urls),
    path('index',views.index),
]
