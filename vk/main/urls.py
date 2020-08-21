from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('accounts/profile/', views.profile),
    path('accounts/', views.index),
]