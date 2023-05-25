from django.shortcuts import render, redirect
from utils.query import query
import uuid

# Authentication

def check_role_redirect(request, expected):

    if get_session_data(request)['role']!= expected:
        role = get_session_data(request)['role']
        if role == 'panitia':
            return '/trigger1/dashboard-panitia/'
        if role == 'manajer':
            return '/trigger1/dashboard-manajer/'
        if role == 'penonton':
            return '/trigger1/dashboard-penonton/'
    return expected

def get_user_id(username):
    id_panitia = query(f"""SELECT id_panitia FROM PANITIA WHERE username='{username}'""")
    id_manajer = query(f"""SELECT id_manajer FROM MANAJER WHERE username='{username}'""")
    id_penonton = query(f"""SELECT id_penonton FROM PENONTON WHERE username='{username}'""")

    if id_panitia != []:
        return str(id_panitia)[25:-4]
    if id_manajer != []:
        return str(id_manajer)[25:-4]
    if id_penonton != []:
        return str(id_penonton)[26:-4]


def get_role(username):
    panitia_check = query(f"""SELECT * FROM PANITIA WHERE username='{username}'""")
    manajer_check = query(f"""SELECT * FROM MANAJER WHERE username='{username}'""")
    penonton_check = query(f"""SELECT * FROM PENONTON WHERE username='{username}'""")

    if panitia_check != []:
        return 'panitia'
    if manajer_check != []:
        return 'manajer'
    if penonton_check != []:
        return 'penonton'
    
def get_session_data(request):
    if not is_authenticated(request):
        return {}
    
    try:
        return {'username': request.session['username'], 'role': request.session['role']}
    except:
        return {}
    
def is_authenticated(request):
    try:
        request.session['username']
        return True
    except KeyError:
        return False

def login_user(request):
    next = request.GET.get("next")
    if is_authenticated(request):
        role = get_role(request.session['username'])
        if role == 'panitia':
            return redirect("/trigger1/dashboard-panitia/")
        if role == 'manajer':
            return redirect("/trigger1/dashboard-manajer/")
        if role == 'penonton':
            return redirect("/trigger1/dashboard-penonton/")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_check = query(f"""SELECT * FROM USER_SYSTEM WHERE username='{username}' and password = '{password}'""") 
        flag = is_authenticated(request)
        if user_check != [] and not flag:
            request.session['username'] = username
            request.session['password'] = password
            request.session['user_id'] = get_user_id(username)
            request.session['role'] = get_role(username)
            request.session.set_expiry(1800)
            request.session.modified = True
            if next != None and next != "None":
                return redirect(next)
            else:
                role = get_role(username)
                if role == 'panitia':
                    return redirect("/trigger1/dashboard-panitia/")
                if role == 'manajer':
                    return redirect("/trigger1/dashboard-manajer/")
                if role == 'penonton':
                    return redirect("/trigger1/dashboard-penonton/")

    return render(request, 'login.html')

def logout_user(request):
    next = request.GET.get('next')

    if not is_authenticated(request):
        return redirect('/trigger1/')

    request.session.flush()
    request.session.clear_expired()

    if next != None and next != 'None':
        return redirect(next)
    else:
        return redirect('/trigger1/')


def register(request):
    return render(request, 'register/register.html')

def register_panitia(request):
    register_url = 'register/register-panitia.html'

    if request.method == 'POST':
        user_id = uuid.uuid1()
        username = request.POST.get('username')
        password = request.POST.get('password')
        nama_depan = request.POST.get('nama_depan')
        nama_belakang = request.POST.get('nama_belakang')
        nomor_hp = request.POST.get('nomor_hp')
        email = request.POST.get('email')
        alamat = request.POST.get('alamat')
        jabatan = request.POST.get('jabatan')
        status = request.POST.getlist('status')

        username_check = query(f"""SELECT * FROM USER_SYSTEM WHERE username='{username}'""")
        if username_check == []:
            query(f"""INSERT INTO USER_SYSTEM VALUES('{username}', '{password}')""")
            query(f"""INSERT INTO NON_PEMAIN VALUES('{user_id}', '{nama_depan}', '{nama_belakang}', '{nomor_hp}', '{email}', '{alamat}')""")
            query(f"""INSERT INTO PANITIA VALUES('{user_id}', '{jabatan}', '{username}')""")
            for i in status:
                query(f"""INSERT INTO STATUS_NON_PEMAIN VALUES('{user_id}', '{i}')""")

            return redirect('/trigger1/login/')
        context = {
            'message' : 'Username sudah pernah terdaftar'
        }
        return render(request, register_url, context)
    context = {
        'message' : 'Username sudah pernah terdaftar'
    }
    return render(request, register_url, context)


def register_manajer(request):
    register_url = 'register/register-manajer.html'

    if request.method == 'POST':
        user_id = uuid.uuid1()
        username = request.POST.get('username')
        password = request.POST.get('password')
        nama_depan = request.POST.get('nama_depan')
        nama_belakang = request.POST.get('nama_belakang')
        nomor_hp = request.POST.get('nomor_hp')
        email = request.POST.get('email')
        alamat = request.POST.get('alamat')
        status = request.POST.getlist('status')

        username_check = query(f"""SELECT * FROM USER_SYSTEM WHERE username='{username}'""")
        if username_check == []:
            query(f"""INSERT INTO USER_SYSTEM VALUES('{username}', '{password}')""")
            query(f"""INSERT INTO NON_PEMAIN VALUES('{user_id}', '{nama_depan}', '{nama_belakang}', '{nomor_hp}', '{email}', '{alamat}')""")
            query(f"""INSERT INTO MANAJER VALUES('{user_id}', '{username}')""")
            for i in status:
                query(f"""INSERT INTO STATUS_NON_PEMAIN VALUES('{user_id}', '{i}')""")

            return redirect('/trigger1/login/')
        
        context = {
            'message' : 'Username sudah pernah terdaftar'
        }
        return render(request, register_url, context)

    context = {
        'message' : 'Username sudah pernah terdaftar'
    }
    return render(request, register_url, context)

def register_penonton(request):
    register_url = 'register/register-penonton.html'

    if request.method == 'POST':
        user_id = uuid.uuid1()
        username = request.POST.get('username')
        password = request.POST.get('password')
        nama_depan = request.POST.get('nama_depan')
        nama_belakang = request.POST.get('nama_belakang')
        nomor_hp = request.POST.get('nomor_hp')
        email = request.POST.get('email')
        alamat = request.POST.get('alamat')
        status = request.POST.getlist('status')

        username_check = query(f"""SELECT * FROM USER_SYSTEM WHERE username='{username}'""")
        if username_check == []:
            query(f"""INSERT INTO USER_SYSTEM VALUES('{username}', '{password}')""")
            query(f"""INSERT INTO NON_PEMAIN VALUES('{user_id}', '{nama_depan}', '{nama_belakang}', '{nomor_hp}', '{email}', '{alamat}')""")
            query(f"""INSERT INTO PENONTON VALUES('{user_id}', '{username}')""")
            for i in status:
                query(f"""INSERT INTO STATUS_NON_PEMAIN VALUES('{user_id}', '{i}')""")

            return redirect('/trigger1/login/')
        
        context = {
            'message' : 'Username sudah pernah terdaftar'
        }
        return render(request, register_url, context)
        
    context = {
        'message' : 'Username sudah pernah terdaftar'
    }
    return render(request, register_url, context)


# Show Pages

def show_home(request):
    context = {
    }
    return render(request, 'home.html', context)

def show_dashboard(request):
    context = {
    }
    return render(request, 'dashboard/dashboard.html', context)

def show_dashboard_panitia(request):
    user_id = request.session['user_id']
    biodata = query(
    f"""
    SELECT nama_depan, nama_belakang, nomor_hp, email, alamat
    FROM NON_PEMAIN 
    WHERE id = '{user_id}'; 
    """
    )
    status = query(
    f"""
    SELECT status
    FROM STATUS_NON_PEMAIN 
    WHERE id_non_pemain = '{user_id}'; 
    """
    )
    jabatan = query(
    f"""
    SELECT jabatan
    FROM PANITIA 
    WHERE id_panitia = '{user_id}'; 
    """
    )
    pertandingan = query(
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
    context = {
        'biodata': biodata,
        'status': status,
        'jabatan': jabatan,
        'pertandingan': pertandingan
    }
    return render(request, 'dashboard/dashboard-panitia.html', context)

def show_dashboard_manajer(request):
    user_id = request.session['user_id']
    biodata = query(
    f"""
    SELECT nama_depan, nama_belakang, nomor_hp, email, alamat
    FROM NON_PEMAIN 
    WHERE id = '{user_id}'; 
    """
    )
    status = query(
    f"""
    SELECT status
    FROM STATUS_NON_PEMAIN 
    WHERE id_non_pemain = '{user_id}'; 
    """
    )
    tim = query(
    f"""
    SELECT T.nama_tim, T.universitas
    FROM TIM_MANAJER as TM, TIM as T
    WHERE T.nama_tim = TM.nama_tim
    AND TM.id_manajer = '{user_id}'; 
    """
    )
    context = {
        'biodata': biodata,
        'status': status,
        'tim': tim
    }
    return render(request, 'dashboard/dashboard-manajer.html', context)

def show_dashboard_penonton(request):
    user_id = request.session['user_id']
    biodata = query(
    f"""
    SELECT nama_depan, nama_belakang, nomor_hp, email, alamat
    FROM NON_PEMAIN 
    WHERE id = '{user_id}'; 
    """
    )
    status = query(
    f"""
    SELECT status
    FROM STATUS_NON_PEMAIN 
    WHERE id_non_pemain = '{user_id}'; 
    """
    )
    context = {
        'biodata': biodata,
        'status': status,
    }
    return render(request, 'dashboard/dashboard-penonton.html', context)