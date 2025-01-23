import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import user_passes_test
from .models import Income, Expense
import calendar
from django.db.models import Sum
import matplotlib.pyplot as plt
from django.db.models.functions import TruncDay
from itertools import chain
from operator import attrgetter

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
        
        # Filter income rocords based on user and month
        user_incomes = Income.objects.filter(
        user=request.user,
        date_received__year=YEAR,
        date_received__month=month_number
        )
        user_expenses = Expense.objects.filter(
        user=request.user,
        date_incurred__year=YEAR,
        date_incurred__month=month_number
        )
        
        transactions = sorted(
            chain(user_incomes, user_expenses),
            key=lambda obj: getattr(obj, 'date_received', None) or getattr(obj, 'date_incurred', None), reverse=True
        )
        
        user_incomes_total = user_incomes.aggregate(total_amount=Sum('amount'))
        user_incomes_total = user_incomes_total['total_amount'] or 0
        user_incomes_total = format(user_incomes_total, '.2f') 
        
        user_expenses_total = user_expenses.aggregate(total_amount=Sum('amount'))
        user_expenses_total = user_expenses_total['total_amount'] or 0
        user_expenses_total = format(user_expenses_total, '.2f') 
        
        # Calculate overall total income and expenses
        total_income = Income.objects.filter(user=request.user).aggregate(total_amount=Sum('amount'))
        total_expenses = Expense.objects.filter(user=request.user).aggregate(total_amount=Sum('amount'))

        total_income_amount = total_income['total_amount'] or 0
        total_expenses_amount = total_expenses['total_amount'] or 0

        # Calculate user balance
        user_balance = total_income_amount - total_expenses_amount
        user_balance = format(user_balance, '.2f')

        return render(request, "finance_tracker/index.html", {
            'month': f"{calendar.month_name[month_number]} {YEAR}",
            'total_income_amount': user_incomes_total,
            'total_expenses_amount': user_expenses_total,
            'user_balance': user_balance,
            'month_name': month_name,
            'transactions' : transactions
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

def password_change(request):
    return render(request, "finance_tracker/password_change/password_change.html")

def password_change_done(request):
    return render(request, "finance_tracker/password_change/password_change_done.html")