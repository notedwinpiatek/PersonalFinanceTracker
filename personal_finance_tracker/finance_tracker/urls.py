from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('account/', views.account_settings, name='account_settings'),
    path('password_change/', views.custom_password_change, name='password_change'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html',redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('income/<str:month_name>/', views.income, name='income'),
    path('expenses/<str:month_name>/', views.expenses, name='expenses'),
    path('<str:month_name>/', views.index, name='index'),
    path('', views.index, name='index'),
]