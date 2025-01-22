from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test

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
        return render(request, 'finance_tracker/months/month_detail.html', {'month_name': month_name})

def income(request):
    return render(request, "finance_tracker/income.html")

def expenses(request):
    return render(request, "finance_tracker/expenses.html")

def account_settings(request):
    return render(request, "finance_tracker/account_settings.html")