from django.contrib.auth import authenticate, login as auth_login,  logout as auth_logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from account.models import User 

import json

@csrf_exempt
def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)

    if user is not None:
        if user.is_active:
            auth_login(request, user)
            
            # Status login sukses.
            return JsonResponse({
                "username": user.username,
                "status": True,
                "message": "Login sukses!",
                "role": user.role,
            }, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": "Login gagal, akun dinonaktifkan."
            }, status=401)

    else:
        return JsonResponse({
            "status": False,
            "message": "Login gagal, periksa kembali email atau kata sandi."
        }, status=401)
    
    
@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data['username']
            password1 = data['password1']
            password2 = data['password2']
            role = data.get('role')  # Ambil role user

            if password1 != password2:
                return JsonResponse({
                    "status": False,
                    "message": "Password tidak cocok."
                }, status=400)

            if User.objects.filter(username=username).exists():
                return JsonResponse({
                    "status": False,
                    "message": "Username sudah digunakan."
                }, status=400)

            # Buat user dengan tipe tertentu
            user = User.objects.create_user(username=username, password=password1)
            user.role = role # Set role user
            user.save()

            return JsonResponse({
                "username": user.username,
                "status": 'success',
                "message": "User berhasil dibuat!"
            }, status=201)

        except KeyError:
            return JsonResponse({
                "status": False,
                "message": "Data tidak lengkap."
            }, status=400)
    else:
        return JsonResponse({
            "status": False,
            "message": "Invalid request method."
        }, status=405)


@csrf_exempt
def logout(request):
    username = request.user.username

    try:
        auth_logout(request)
        return JsonResponse({
            "username": username,
            "status": True,
            "message": "Logout berhasil!"
        }, status=200)
    except:
        return JsonResponse({
        "status": False,
        "message": "Logout gagal."
        }, status=401)