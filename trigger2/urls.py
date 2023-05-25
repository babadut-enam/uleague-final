from django.urls import path
from trigger2.views import show_pilih_pemain, show_pilih_pelatih, show_mengelola_tim

app_name = 'trigger2'

urlpatterns = [
    path('pilih-pemain/', show_pilih_pemain, name='pilih-pemain'),
    path('pilih-pelatih/', show_pilih_pelatih, name='pilih-pelatih'),
    path('mengelola-tim/', show_mengelola_tim, name='mengelola-tim'),
]