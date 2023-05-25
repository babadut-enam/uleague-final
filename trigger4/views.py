from django.shortcuts import redirect, render

from trigger1.views import check_role_redirect, get_role, is_authenticated
from utils.query import query

def show_list_pertandingan(request):
    if not is_authenticated(request):
        return redirect('/trigger1/login/?next=/trigger4/list-pertandingan/')
    if check_role_redirect(request, 'panitia') != 'panitia':
        return redirect(check_role_redirect(request, 'panitia'))


    user_id = request.session['user_id']
    data = {}
    data['pertandingan'] = query(
        f"""
        SELECT TP.nama_tim, S.nama, P.start_datetime 
        FROM PERTANDINGAN as P, TIM_PERTANDINGAN as TP, STADIUM as S
        WHERE P.id_pertandingan = TP.id_pertandingan
        AND S.id_stadium = P.stadium
        ORDER BY P.start_datetime ASC;
        """
        )

    return render(request, 'list-pertandingan.html', {'data': data})

def show_pembuatan_pertandingan(request):
    context = {
    }
    return render(request, "pembuatan-pertandingan.html", context)

def show_form_pembuatan_pertandingan(request):
    context = {
    }
    return render(request, "form-pembuatan-pertandingan.html", context)

#@login_required(login_url='/sepakbola/login/')
def show_form_pemilihan_jadwal(request):
    context = {
    }
    return render(request, "form-pemilihan-jadwal.html", context)