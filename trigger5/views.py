from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
#@login_required(login_url='/sepakbola/login/')
def show_manage_pertandingan(request):
    context = {
    }
    return render(request, "manage-pertandingan.html", context)

#@login_required(login_url='/sepakbola/login/')
def show_peristiwa_tim(request):
    context = {
    }
    return render(request, "peristiwa-tim.html", context)

#@login_required(login_url='/sepakbola/login/')
def mulai_pertandingan(request):
  user = request.user
  context = {
    }
  return render(request, "mulai-pertandingan.html", context)

#@login_required(login_url='/sepakbola/login/')
def tim1_peristiwa(request):
  user = request.user
  context = {
    }
  return render(request, "tim1-peristiwa.html", context)

#@login_required(login_url='/sepakbola/login/')
def tim2_peristiwa(request):
  user = request.user
  context = {
    }
  return render(request, "tim2-peristiwa.html", context)