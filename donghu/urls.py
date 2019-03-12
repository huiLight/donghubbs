from django.urls import path
from . import views

app_name = 'donghu'
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('sendcode/', views.sendcode, name='sendcode'),
    path('sendcode/code', views.identifycode, name="identifycode"),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout')
]