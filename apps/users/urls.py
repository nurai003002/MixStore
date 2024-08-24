from django.urls import path
from apps.users.views import checkout, login1, register, user_logout,confirm,forgot_password,reset_password

urlpatterns = [
    path('checkout/',  checkout, name='checkout'),
    path('login/', login1, name='user_login'),
    path('register/', register, name='user_register'),
    path('logout/', user_logout, name='user_logout'),
    path('confirm/', confirm, name='confirm'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('reset_password/', reset_password, name='reset_password'),
]