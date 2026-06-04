from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect

urlpatterns = [
    # 🔥 ROOT FIX
    path('', lambda request: redirect('/index')),

    # admin
    path('admin/', admin.site.urls),

    # app routes
    path('', include('pred_app.urls')),

    # auth
    path('login/', auth_views.LoginView.as_view(template_name='pred_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/index'), name='logout'),
]