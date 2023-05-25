from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from trigger1.views import check_role_redirect, get_role, is_authenticated

@csrf_exempt
#@login_required(login_url='/sepakbola/login/')
def pembelian_tiket(request):
  user = request.user
  context = {
    }
  return render(request, "pembelian-tiket.html", context)

@csrf_exempt
#@login_required(login_url='/sepakbola/login/')
def pembelian_tiket2(request):
  user = request.user
  context = {
    }
  return render(request, "pembelian-tiket2.html", context)

@csrf_exempt
#@login_required(login_url='/sepakbola/login/')
def pembelian_tiket3(request):
  user = request.user
  context = {
    }
  return render(request, "pembelian-tiket3.html", context)

@csrf_exempt
#@login_required(login_url='/sepakbola/login/')
def pembelian_tiket4(request):
  user = request.user
  context = {
    }
  return render(request, "pembelian-tiket4.html", context)

def show_history_rapat(request):
    if not is_authenticated(request):
        return redirect('/trigger1/login/?next=/trigger3/history-rapat/')
    if check_role_redirect(request, 'panitia') != 'panitia':
        return redirect(check_role_redirect(request, 'panitia'))
    context = {
    }
    return render(request, "rapat/history-rapat.html", context)
