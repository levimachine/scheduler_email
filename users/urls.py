from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.forms import LoginForm
from users.views import UserRegisterView, UserInputSecretKey

app_name = UsersConfig.name

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user_register'),
    path('login/', LoginView.as_view(template_name='users/user_login.html', form_class=LoginForm), name='user_login'),
    path('logout/', LogoutView.as_view(), name='user_logout'),
    path('user_verify/<int:pk>', UserInputSecretKey.as_view(), name='user_verify'),
]
