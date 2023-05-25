from django.urls import path
from trigger3.views import show_peminjaman_stadium, show_form_peminjaman_stadium, show_list_waktu_stadium
from trigger3.views import form_isi_rapat, mulai_rapat

app_name = 'trigger3'

urlpatterns = [
    path('waktu-stadium/', show_list_waktu_stadium, name='waktu-stadium'),
    path('peminjaman-stadium/', show_peminjaman_stadium, name='peminjaman-stadium'),
    path('form-peminjaman-stadium/', show_form_peminjaman_stadium, name='form-peminjaman-stadium'),
    path('form-isi-rapat/', form_isi_rapat, name='form-isi-rapat'),
    path('mulai-rapat/', mulai_rapat, name='mulai-rapat'),
]