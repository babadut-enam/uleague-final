from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
#@login_required(login_url='/sepakbola/login/')
def show_mengelola_tim(request):
    context = {
    }
    return render(request, "mengelola-tim.html", context)

#@login_required(login_url='/sepakbola/login/')
def show_pilih_pemain(request):
    context = {
    }
    return render(request, "pilih-pemain.html", context)

#@login_required(login_url='/sepakbola/login/')
def show_pilih_pelatih(request):
    context = {
    }
    return render(request, "pilih-pelatih.html", context)

