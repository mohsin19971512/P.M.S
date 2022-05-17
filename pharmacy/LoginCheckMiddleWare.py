from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import admin
import datetime


from django.core.cache import cache
from django.conf import settings


#Check whether the user is logged in or not

class LoginCheckMiddleWare(MiddlewareMixin):
   
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        user = request.user

        if user.is_authenticated:
            if user.user_type == "1":
                
                if modulename == "pharmacy.HODViews": 
                    pass
                elif modulename == "":
                    pass
                elif modulename == "pharmacy.views" or modulename == "django.views.static":
                    pass
                else:
                    pass
            
            else:
                return redirect("login")

            
        else:
            if request.path == reverse("login"):
                pass
            else:
                return redirect("login")

