from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html',redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('months/<str:month_name>/', views.month, name='month'),
    path('income/', views.income, name='income'),
    path('expenses/', views.expenses, name='expenses'),
    path('account/', views.account_settings, name='account_settings'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_change/password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),
    
]