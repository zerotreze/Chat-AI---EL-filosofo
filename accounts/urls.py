from django.urls import path
from django.contrib.auth import views

from accounts.views import RegisterView


urlpatterns = [
    path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('accounts/register/', RegisterView.as_view(), name='register'),
    path('accounts/logout/', views.LogoutView.as_view(), name='logout'),
]