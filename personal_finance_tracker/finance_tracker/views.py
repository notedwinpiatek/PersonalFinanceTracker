import datetime
import json
import calendar
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import user_passes_test, login_required
from .models import Income, Expense
from .forms import CustomPasswordChangeForm, IncomeForm, ExpenseForm
from django.db.models import Sum
from itertools import chain

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
        
        # Initialize monthly data arrays
        income_data = [0.0] * 12
        expense_data = [0.0] * 12
        
         # Fetch all income and expense records for the entire year
        all_user_incomes = Income.objects.filter(user=request.user, date_received__year=YEAR)
        all_user_expenses = Expense.objects.filter(user=request.user, date_incurred__year=YEAR)

        # Group and aggregate income and expense data for the entire year
        monthly_income = all_user_incomes.values('date_received__month').annotate(total=Sum('amount'))
        monthly_expenses = all_user_expenses.values('date_incurred__month').annotate(total=Sum('amount'))

        # Populate the monthly data arrays
        for income in monthly_income:
            income_data[income['date_received__month'] - 1] = float(income['total'])
        for expense in monthly_expenses:
            expense_data[expense['date_incurred__month'] - 1] = float(expense['total'])
            
        return render(request, "finance_tracker/index.html", {
            'month': f"{calendar.month_name[month_number]} {YEAR}",
            'total_income_amount': user_incomes_total,
            'total_expenses_amount': user_expenses_total,
            'user_balance': user_balance,
            'month_name': month_name,
            'transactions' : transactions,
            'income_data': json.dumps(income_data),
            'expense_data': json.dumps(expense_data),
            'months': VALID_MONTHS,
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


@login_required
def income(request, month_name=None):
    # Handle the current month if no month name is provided
    if not month_name:
        month_name = datetime.datetime.now().strftime('%b') 

    # Convert the month name to a month number
    month_number = list(calendar.month_abbr).index(month_name)

    # Filter and sort income records based on user and month
    user_incomes = Income.objects.filter(
        user=request.user,
        date_received__year=YEAR,
        date_received__month=month_number
    ).order_by('-date_received', '-time_received')

    # Handle the form submission
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            # Save the form instance but assign the logged-in user
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            return redirect('income', month_name=month_name)
    else:
        form = IncomeForm()

    return render(request, "finance_tracker/income.html", {
        'month': f"{calendar.month_name[month_number]} {YEAR}",
        'incomes': user_incomes,
        'form': form,
        'months': VALID_MONTHS,
        'month_name': month_name
    })


@login_required
def expenses(request, month_name=None):
    # Handle the current month if no month name is provided
    if not month_name:
        month_name = datetime.datetime.now().strftime('%b') 
        
    # Convert the month name to a month number
    month_number = list(calendar.month_abbr).index(month_name.capitalize())

    # Handle the form submission
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            
            expense = form.save(commit=False)
            expense.user = request.user  
            expense.save()
            return redirect('expenses', month_name=calendar.month_abbr[month_number])  
    else:
        form = ExpenseForm()  

    # Filter and sort expense records based on user and month
    user_expenses = Expense.objects.filter(
        user=request.user,
        date_incurred__year=YEAR,
        date_incurred__month=month_number
    ).order_by('-date_incurred', '-time_incurred')

    return render(request, "finance_tracker/expenses.html", {
        'month': f"{calendar.month_name[month_number]} {YEAR}",
        'expenses': user_expenses,
        'form': form,
        'months': VALID_MONTHS,
        'month_name': month_name
    })


@login_required
def account_settings(request):
    return render(request, "finance_tracker/account_settings.html")


@login_required
def custom_password_change(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return render(request, 'registration/password_change_done.html')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'registration/password_change.html', {'form': form})
