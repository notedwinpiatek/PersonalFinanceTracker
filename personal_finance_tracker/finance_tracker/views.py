import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test
from .models import Income
import calendar

# Create your views here.
def index(request):
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


def month(request, month_name):
    valid_months = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]
    if month_name not in valid_months:
        return render(request, {'message': 'Invalid month selected.'})
    else:
        month_number = list(calendar.month_abbr).index(month_name)
        year = datetime.datetime.now().year
        
        # Filter income rocords based on user and month
        user_incomes = Income.objects.filter(
        user=request.user,
        date_received__year=year,
        date_received__month=month_number
        )
        
        return render(request, 'finance_tracker/months/month_detail.html', {
        'month': f"{calendar.month_name[month_number]} {year}"
    })

def income(request, month_name):
    valid_months = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]
    
    if month_name not in valid_months:
        return render(request, {'message': 'Invalid month selected.'})
    else:
        month_number = list(calendar.month_abbr).index(month_name)
        year = datetime.datetime.now().year
        
        # Filter income rocords based on user and month
        user_incomes = Income.objects.filter(
        user=request.user,
        date_received__year=year,
        date_received__month=month_number
        )
        
    return render(request, "finance_tracker/income.html", {
        'month': f"{calendar.month_name[month_number]} {year}",
        'incomes': user_incomes
    })

def expenses(request):
    return render(request, "finance_tracker/expenses.html")