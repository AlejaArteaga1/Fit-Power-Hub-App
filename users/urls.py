from django.urls import path
from django.contrib.auth import views as auth_views
from store.forms import UserRegistrationForm
from store.views import profile_view

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='store/register.html'), name='register'),
]