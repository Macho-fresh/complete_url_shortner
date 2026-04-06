from django.contrib import admin
from django.urls import path
from .views import UrlView, redirect_url, show_url, update_url

urlpatterns = [
    path('url/', UrlView.as_view()),
    path('<str:shorturl>/', redirect_url),
    path('url/<int:id>/', show_url.as_view()),
    path('url/update/<int:id>', update_url.as_view()),


]