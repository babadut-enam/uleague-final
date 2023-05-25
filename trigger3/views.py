from django.shortcuts import redirect, render

from trigger1.views import check_role_redirect, get_role, is_authenticated
from utils.query import query
import datetime

def show_peminjaman_stadium(request):
    if not is_authenticated(request):
        return redirect('/trigger1/login/?next=/trigger3/peminjaman-stadium/')
    if check_role_redirect(request, 'manajer') != 'manajer':
        return redirect(check_role_redirect(request, 'manajer'))


    user_id = request.session['user_id']
    data = {}
    data['peminjaman'] = query(
        f"""
        SELECT nama, start_datetime, end_datetime
        FROM STADIUM as S, PEMINJAMAN as P
        WHERE S.id_stadium = P.id_stadium
        AND P.id_manajer = '{user_id}';
        """
        )

    return render(request, 'peminjaman-stadium.html', {'data': data})

def show_form_peminjaman_stadium(request):
    form_url = 'form-peminjaman-stadium.html'
    request.session['id_stadium'] = ''
    request.session['stadium'] = ''
    request.session['date'] = ''

    if not is_authenticated(request):
        return redirect('/trigger1/login/?next=/trigger3/peminjaman-stadium/')
    if check_role_redirect(request, 'manajer') != 'manajer':
        return redirect(check_role_redirect(request, 'manajer'))

    data = {}
    data['messages'] = ''
    data['tersedia'] = query('SELECT nama FROM STADIUM;')
    
    if request.method == 'POST':
        stadium = request.POST.get('stadium')
        date = request.POST.get('date')

        print('---')
        print(stadium)
        print(date)
        print('---')

        if stadium == None or date == '':
            data['messages'] = 'Ada pilihan yang belum terisi!'
            return render(request, form_url, {'data': data})
        elif stadium != None and date != '':
            id_stadium = query(
                f"""
                SELECT id_stadium 
                FROM STADIUM 
                WHERE nama = '{stadium}'; 
                """
                )
            waktu_check = query(
                f"""
                SELECT P.id_stadium 
                FROM PEMINJAMAN as P, STADIUM as S 
                WHERE P.id_stadium = S.id_stadium
                AND S.nama = '{stadium}'
                AND P.id_stadium = '{str(id_stadium)[25:-4]}'
                AND P.start_datetime::date = '{date}'; 
                """
                )

            print('---')
            print(str(id_stadium)[25:-4])
            print(waktu_check)
            print(request.session['user_id'])
            print('---')

            if waktu_check != []:
                data['messages'] = 'Stadium sudah dipesan pada waktu tersebut!'
                return render(request, form_url, {'data': data})
            else :
                request.session['id_stadium'] = str(id_stadium)[25:-4]
                request.session['stadium'] = stadium
                request.session['date'] = date
                return redirect('/trigger3/waktu-stadium/')

    return render(request, form_url, {'data': data})

def show_list_waktu_stadium(request):
    if not is_authenticated(request):
        return redirect('/trigger1/login/?next=/trigger3/peminjaman-stadium/')
    if check_role_redirect(request, 'manajer') != 'manajer':
        return redirect(check_role_redirect(request, 'manajer'))

    if request.method == 'POST':
        date = request.session['date']
        id_stadium = request.session['id_stadium']

        time = request.POST.get('waktu')
        start_datetime = date + " " + time[14:-18]
        end_datetime = date + " " + time[30:-2]

        print('---')
        print(date)
        print(id_stadium)
        print(start_datetime)
        print(end_datetime)
        print('---')

        query(f"""INSERT INTO PEMINJAMAN VALUES ('{request.session['user_id']}', '{start_datetime}', '{end_datetime}', '{id_stadium}')""")
        return redirect("/trigger3/peminjaman-stadium/")

    data = {}
    data['stadium'] = request.session['stadium']
    data['waktu'] = query(
        f"""
        SELECT *
        FROM (
            SELECT '07:00:00' start, '09:00:00' end UNION 
            SELECT '10:00:00', '12:00:00' UNION 
            SELECT '13:00:00', '15:00:00' UNION
            SELECT '16:00:00', '18:00:00' UNION 
            SELECT '18:00:00', '21:00:00'
        ) TEMP 
        WHERE (TEMP.start, TEMP.end) 
        NOT IN (
            SELECT start_datetime::time::varchar, end_datetime::time::varchar 
            FROM PEMINJAMAN
            WHERE start_datetime::date = '{request.session['date']}'
            AND id_stadium = '{request.session['id_stadium']}'
        )
        ORDER BY start
        """
        )
    
    print("---")
    print(data['waktu'])
    print("---")

    return render(request, 'list-waktu-stadium.html', {'data': data})

def mulai_rapat(request):
    request.session['id_pertandingan'] = ''

    if not is_authenticated(request):
        return redirect('/trigger1/login/?next=/trigger3/mulai-rapat/')
    if check_role_redirect(request, 'panitia') != 'panitia':
        return redirect(check_role_redirect(request, 'panitia'))

    data = {}
    data['messages'] = ''
    data['pertandingan'] = query(
        """
        SELECT P.id_pertandingan, T.tim_a, T.tim_b, S.nama stadium, P.start_datetime
        FROM PERTANDINGAN P
        NATURAL JOIN
        (SELECT A.id_pertandingan, A.nama_tim tim_a, B.nama_tim tim_b
        FROM TIM_PERTANDINGAN A JOIN TIM_PERTANDINGAN B
        ON A.id_pertandingan = B.id_pertandingan
        WHERE A.nama_tim < B.nama_tim) T
        JOIN STADIUM S ON S.id_stadium = P.stadium
        WHERE P.id_pertandingan NOT IN(SELECT id_pertandingan FROM RAPAT);
        """
        )
    
    if request.method == 'POST':
        request.session['id_pertandingan'] = request.POST.get('mulai')
        print(request.session['id_pertandingan'])
        return redirect('/trigger3/form-isi-rapat/')

    return render(request, "rapat/mulai-rapat.html", {'data': data})

def form_isi_rapat(request):
    id_pertandingan = request.session['id_pertandingan']
    user_id = request.session['user_id']

    if not is_authenticated(request):
        return redirect('/trigger1/login/?next=/trigger3/form-isi-rapat/')
    if check_role_redirect(request, 'panitia') != 'panitia':
        return redirect(check_role_redirect(request, 'panitia'))

    data = {}
    data['messages'] = ''
    data['pertandingan'] = query(
        f"""
        SELECT A.nama_tim tim_a, B.nama_tim tim_b
        FROM TIM_PERTANDINGAN A JOIN TIM_PERTANDINGAN B
        ON A.id_pertandingan = B.id_pertandingan
        WHERE A.nama_tim < B.nama_tim
        AND A.id_pertandingan = '{id_pertandingan}';
        """
        )
    
    if request.method == 'POST':
        isi_rapat = request.POST.get('isi_rapat')
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tim_a = query(
            f"""
            SELECT T.tim_a
            FROM PERTANDINGAN P
            NATURAL JOIN
            (SELECT A.id_pertandingan, A.nama_tim tim_a, B.nama_tim tim_b
            FROM TIM_PERTANDINGAN A JOIN TIM_PERTANDINGAN B
            ON A.id_pertandingan = B.id_pertandingan
            WHERE A.nama_tim < B.nama_tim AND A.id_pertandingan = '{id_pertandingan}') T
            JOIN STADIUM S ON S.id_stadium = P.stadium
            WHERE P.id_pertandingan NOT IN(SELECT id_pertandingan FROM RAPAT);
            """
            )
        tim_b = query(
            f"""
            SELECT T.tim_b
            FROM PERTANDINGAN P
            NATURAL JOIN
            (SELECT A.id_pertandingan, A.nama_tim tim_a, B.nama_tim tim_b
            FROM TIM_PERTANDINGAN A JOIN TIM_PERTANDINGAN B
            ON A.id_pertandingan = B.id_pertandingan
            WHERE A.nama_tim < B.nama_tim AND A.id_pertandingan = '{id_pertandingan}') T
            JOIN STADIUM S ON S.id_stadium = P.stadium
            WHERE P.id_pertandingan NOT IN(SELECT id_pertandingan FROM RAPAT);
            """
            )
        manajer_a = query(
            f"""
            SELECT id_manajer::text
            FROM TIM_MANAJER
            WHERE nama_tim = '{tim_a[0][0]}';
            """
            )
        manajer_b = query(
            f"""
            SELECT id_manajer::text
            FROM TIM_MANAJER
            WHERE nama_tim = '{tim_b[0][0]}';
            """
            )
        query(f"""INSERT INTO RAPAT VALUES ('{id_pertandingan}', '{date}', '{user_id}', '{manajer_a[0][0]}', '{manajer_b[0][0]}', '{isi_rapat[0][0]}')""")
        return redirect("/trigger3/mulai-rapat/")


    return render(request, "rapat/form-isi-rapat.html", {'data': data})