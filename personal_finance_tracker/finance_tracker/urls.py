from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html',redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('income/<str:month_name>/', views.income, name='income'),
    path('expenses/<str:month_name>/', views.expenses, name='expenses'),
    path('<str:month_name>/', views.index, name='index'),
    path('', views.index, name='index'),
    path('account/', views.account_settings, name='account_settings'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_change/password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),
    
]