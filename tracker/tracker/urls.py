"""tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('registerpackage/', views.registerpackageform),
    path('addregisterpackage', views.addregisterpackage),
    path('register/', views.registerform),
    path('addregister', views.addregister),
    path('login/', views.loginform),
    path('addlogin', views.addlogin),
    path('logout/', views.logout),
    path('generate/', views.generateform),
    path('addgenerate', views.generate),
    path('track/', views.trackform),
    path('addtrack', views.addtrack),
    path('activate', views.activateform),
    path('addactivate', views.addactivate),
    path('avaliablecode', views.avaliablecode),
    path('registeredcode', views.registeredcode),
    path('trackqr/', views.trackqrform),
    path('addtrackqr', views.addtrackqr),
    path('registerpackageqr', views.registerpackageqrform),
    path('addregisterpackageqr', views.addregisterpackageqr),
    path('activateqr', views.activateqrform),
    path('addactivateqr', views.addactivateqr),
]
