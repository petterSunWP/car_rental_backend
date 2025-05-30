from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from service.models import User
from django.contrib.auth.hashers import make_password
# views/auth_views.py

from django.contrib.auth import login
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password
from django.shortcuts import redirect

@csrf_exempt
def login_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
        print(username,password)
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({"success": False, "error": "Invalid username or password"}, status=401)

        if check_password(password, user.password):
            # Django 的 login 只支持 auth.User，所以你不能用 login() —— 建议用 session 处理登录
            request.session["user_id"] = user.id
            request.session["username"] = user.username
            request.session["role"] = user.role
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "error": "Invalid username or password"}, status=401)

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def register_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        role = data.get("role", "Customer")

        if User.objects.filter(username=username).exists():
            return JsonResponse({"success": False, "error": "Username already taken"}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({"success": False, "error": "Email already in use"}, status=400)

        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password),  # 加密密码
            role=role
        )

        return JsonResponse({"success": True, "user_id": user.id})
    return JsonResponse({"error": "Method not allowed"}, status=405)

def check_auth(request):
    is_logged_in = bool(request.session.get("user_id"))
    return JsonResponse({"is_authenticated": is_logged_in})



def logout_view(request):
    request.session.flush()  # 清除所有登录信息
    return redirect("/service")     # 回到首页
