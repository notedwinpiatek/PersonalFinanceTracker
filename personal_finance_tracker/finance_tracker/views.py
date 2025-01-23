import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import user_passes_test
from .models import Income, Expense

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import CustomPasswordChangeForm

import calendar

VALID_MONTHS = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]

YEAR = datetime.datetime.now().year

# Create your views here.
def index(request, month_name=None):
    if request.user.is_authenticated:
        if not month_name:
            month_name = datetime.datetime.now().strftime('%b') 
        
        month_number = list(calendar.month_abbr).index(month_name)
            
        return render(request, "finance_tracker/index.html", {
            'month': f"{calendar.month_name[month_number]} {YEAR}"
        })
    else:
        return render(request, "finance_tracker/index.html")

def not_logged_in(user):
    return not user.is_authenticated

@user_passes_test(not_logged_in, login_url='/finance_tracker', redirect_field_name=None)  
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def income(request, month_name):
    if not month_name:
        month_name = datetime.now().strftime('%b') 
    else:
        month_number = list(calendar.month_abbr).index(month_name)
        
        # Filter income rocords based on user and month
        user_incomes = Income.objects.filter(
        user=request.user,
        date_received__year=YEAR,
        date_received__month=month_number
        )
        
    return render(request, "finance_tracker/income.html", {
        'month': f"{calendar.month_name[month_number]} {YEAR}",
        'incomes': user_incomes
    })

def expenses(request, month_name):
    if not month_name:
        month_name = datetime.now().strftime('%b') 
    else:
        month_number = list(calendar.month_abbr).index(month_name)
        
        # Filter income rocords based on user and month
        user_expenses = Expense.objects.filter(
        user=request.user,
        date_incurred__year=YEAR,
        date_incurred__month=month_number
        )
        
    return render(request, "finance_tracker/expenses.html", {
        'month': f"{calendar.month_name[month_number]} {YEAR}",
        'expenses': user_expenses
    })


def account_settings(request):
    return render(request, "finance_tracker/account_settings.html")


@login_required
def custom_password_change(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('password_change_done')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'registration/password_change.html', {'form': form})
