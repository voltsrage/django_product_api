from django.contrib import admin
from django.urls import path,include

from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
		path('',views.api_home),
		path('create/',views.api_home_save),
		path('auth/',obtain_auth_token)
]