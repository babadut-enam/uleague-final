from django.urls import path
from trigger4.views import show_list_pertandingan, show_pembuatan_pertandingan, show_form_pembuatan_pertandingan, show_form_pemilihan_jadwal

app_name = 'trigger4'

urlpatterns = [
    path('list-pertandingan/', show_list_pertandingan, name='list-pertandingan'),
    path('pembuatan-pertandingan/', show_pembuatan_pertandingan, name='pembuatan-pertandingan'),
    path('pembuatan-pertandingan/form-pembuatan-pertandingan/', show_form_pembuatan_pertandingan, name='form-pembuatan-pertandingan'),
    path('pembuatan-pertandingan/form-pemilihan-jadwal/', show_form_pemilihan_jadwal, name='form-pemilihan-jadwal'),
]