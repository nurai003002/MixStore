from django.urls import path
from apps.users.views import checkout, login1, register, user_logout,confirm

urlpatterns = [
    path('checkout/',  checkout, name='checkout'),
    path('login/', login1, name='user_login'),
    path('register/', register, name='user_register'),
    path('logout/', user_logout, name='user_logout'),
    path('confirm/', confirm, name='confirm'),
]