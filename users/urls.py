from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('login/', views.log_in, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('registration/', views.registration, name='registration'),
    path('registration_success/', views.registration_success, name='registration success')
]
