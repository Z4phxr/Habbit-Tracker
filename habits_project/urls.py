from django.contrib import admin
from django.urls import path, include
from base import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path("api/", include("api.urls")),
    path('track/<str:section>/<str:period>/', views.tracker, name='tracker'),
    path('track/edit/', views.edit_habits, name='edit_habits'),
]
