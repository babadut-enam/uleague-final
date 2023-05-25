from django.urls import path
from trigger1.views import login_user, logout_user
from trigger1.views import register, register_manajer, register_penonton, register_panitia
from trigger1.views import show_home, show_dashboard, show_dashboard_manajer, show_dashboard_panitia, show_dashboard_penonton

app_name = 'trigger1'

urlpatterns = [
    path('', show_home, name='home'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register, name='register'),
    path('register-manajer/', register_manajer, name='register-manajer'),
    path('register-penonton/', register_penonton, name='register-penonton'),
    path('register-panitia/', register_panitia, name='register-panitia'),
    path('dashboard/', show_dashboard, name='dashboard'),
    path('dashboard-manajer/', show_dashboard_manajer, name='dashboard-manajer'),
    path('dashboard-panitia/', show_dashboard_panitia, name='dashboard-panitia'),
    path('dashboard-penonton/', show_dashboard_penonton, name='dashboard-penonton'),
]