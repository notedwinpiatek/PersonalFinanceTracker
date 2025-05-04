from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('api/set_currency/', views.set_currency, name="set_currency"),
    path('landing_page/', views.landing_page, name='landing_page'),
    path('select_gender/', views.select_gender, name='select_gender'),
    path('sources/<str:month_name>/', views.sources, name='sources'),
    path('sources/', views.sources, name='sources'),
    path('spendings/<str:month_name>/', views.spendings, name='spendings'),
    path('spendings/', views.spendings, name='spendings'),
    path('account/', views.account_settings, name='account_settings'),
    path('password_change/', views.custom_password_change, name='password_change'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html',redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('income/<str:month_name>/', views.income, name='income'),
    path('income/', views.income, name='income'),
    path('expenses/<str:month_name>/', views.expenses, name='expenses'),
    path('expenses/', views.expenses, name='expenses'),
    path('<str:month_name>/', views.index, name='index'),
    path('', views.index, name='index'),
]