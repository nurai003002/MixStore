from django.urls import path
from apps.users.views import login1, register, user_logout

urlpatterns = [
    path('login/', login1, name='user_login'),
    path('register/', register, name='user_register'),
    path('logout/', user_logout, name='user_logout'),
]