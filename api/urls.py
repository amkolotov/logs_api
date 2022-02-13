from django.urls import path

from api import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('get-token/', views.get_token, name='get_token'),
    path('get-logs/', views.get_logs, name='get_logs'),
]
