from django.urls import path
from . import views

urlpatterns = [path("", views.hello), path("generate/", views.generate)]
