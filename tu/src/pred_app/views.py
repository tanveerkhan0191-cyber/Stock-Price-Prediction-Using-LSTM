from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .lstm_model import lstm_prediction
import json


# 🔥 HOME
def index(request):
    return render(request, 'pred_app/index.html')


# 🔥 PREDICTION
@login_required(login_url='login')
def pred(request):
    result = None

    if request.method == "POST":
        stock = request.POST.get('stock')
        print("STOCK:", stock)

        try:
            data = lstm_prediction("NSE", stock)
            parsed = json.loads(data)

            print("PARSED:", parsed)

            # ✅ SAFE ERROR CHECK
            if isinstance(parsed, dict) and "error" in parsed:
                result = {"error": parsed["error"]}
            else:
                result = parsed[-1]

        except Exception as e:
            print("VIEW ERROR:", e)
            result = {"error": "Prediction failed"}

    return render(request, 'pred_app/pred.html', {'result': result})


# 🔥 CONTACT
def contact(request):
    return render(request, 'pred_app/contact.html')


# 🔥 REGISTER
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return render(request, 'pred_app/register.html', {
                'error': 'Username already exists'
            })

        User.objects.create_user(username=username, password=password)
        return redirect('login')

    return render(request, 'pred_app/register.html')