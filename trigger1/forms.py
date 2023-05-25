from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password1 = forms.CharField(max_length=50)
    password2 = forms.CharField(max_length=50)
    
class RegisterForm(UserCreationForm):
    CHOICES = [('Mahasiswa', 'Mahasiswa'), ('Dosen', 'Dosen'), ('Tendik', 'Tendik'), ('Alumni', 'Alumni'), ('Umum', 'Umum'),]

    username = forms.CharField(max_length=50)
    password1 = forms.CharField(max_length=50)
    password2 = forms.CharField(max_length=50)
    nama_depan = forms.CharField(max_length=50)
    nama_belakang = forms.CharField(max_length=50)
    nomor_hp = forms.CharField(max_length=15)
    email = forms.CharField(max_length=50)
    alamat = forms.CharField(max_length=255)
    status = forms.CharField(
        widget=forms.RadioSelect(choices=CHOICES)
    )
    jabatan = forms.CharField(max_length=50, required=False)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'nama_depan', 'nama_belakang', 'nomor_hp', 'email',  'status', 'alamat', 'is_manajer', 'is_penonton', 'is_panitia' )