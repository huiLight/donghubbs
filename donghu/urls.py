from django.urls import path
from . import views

app_name = 'donghu'
urlpatterns = [
    path('', views.index, name='index'),
]