from django.urls import path
from trigger5.views import show_manage_pertandingan, show_peristiwa_tim, mulai_pertandingan, tim1_peristiwa, tim2_peristiwa

app_name = 'trigger5'

urlpatterns = [
    path('manage-pertandingan/', show_manage_pertandingan, name='manage-pertandingan'),
    path('manage-pertandingan/peristiwa-tim/', show_peristiwa_tim, name='peristiwa-tim'),
    path('mulai-pertandingan/', mulai_pertandingan, name='mulai_pertandingan'),
    path('tim1-peristiwa/', tim1_peristiwa, name='tim1_peristiwa'),
    path('tim2-peristiwa/', tim2_peristiwa, name='tim2_peristiwa'),
]