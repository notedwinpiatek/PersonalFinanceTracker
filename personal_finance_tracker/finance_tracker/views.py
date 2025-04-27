import datetime
import json
import calendar
from django.urls import reverse
from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import update_session_auth_hash, login
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from .models import Income, Expense
from .forms import CustomPasswordChangeForm, IncomeForm, ExpenseForm, ExpenseCategory, IncomeSource, UserProfile, GenderSelectionForm, IncomeSourceForm, ExpenseCategoryForm
from django.db.models import Sum
from itertools import chain
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import messages

VALID_MONTHS = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]

YEAR = datetime.datetime.now().year

@login_required
def index(request, month_name=None):
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

    gender = UserProfile.objects.filter(user=request.user).values('gender')[0]['gender']

    # Group and aggregate income and expense data for the entire year
    monthly_income = all_user_incomes.values('date_received__month').annotate(total=Sum('amount'))
    monthly_expenses = all_user_expenses.values('date_incurred__month').annotate(total=Sum('amount'))

    # Populate the monthly data arrays
    for income in monthly_income:
        income_data[income['date_received__month'] - 1] = float(income['total'])
    for expense in monthly_expenses:
        expense_data[expense['date_incurred__month'] - 1] = float(expense['total'])
        
    # Filter income sources by month
    income_sources = Income.objects.filter(
        user=request.user,
        date_received__year=YEAR,
        date_received__month=month_number
    ).values('source__name').annotate(total=Sum('amount'))
    
    source_labels = [source['source__name'] for source in income_sources]
    source_totals = [float(source['total']) for source in income_sources]
    
    categories = ExpenseCategory.objects.filter(user=request.user)
    other_category = ExpenseCategory.objects.get(user=request.user, name='Other')
    
    categories = list(categories)  # Convert queryset to list (if needed)
    categories.sort(key=lambda category: category.name == "Other") 
    
    # Filter income sources by month
    expense_categories = Expense.objects.filter(
        user=request.user,
        date_incurred__year=YEAR,
        date_incurred__month=month_number
    ).values('category__name').annotate(total=Sum('amount'))
    
    category_labels = [category['category__name'] for category in expense_categories]
    category_totals = [float(category['total']) for category in expense_categories]
        
    return render(request, "finance_tracker/index.html", {
        'month': f"{calendar.month_name[month_number]} {YEAR}",
        'total_income_amount': user_incomes_total,
        'total_expenses_amount': user_expenses_total,
        'user_balance': user_balance,
        'month_name': month_name,
        'transactions' : transactions,
        'income_data': json.dumps(income_data),
        'expense_data': json.dumps(expense_data),
        'months_labels': json.dumps(VALID_MONTHS),
        'months': VALID_MONTHS,
        'gender': gender,
        'source_labels': json.dumps(source_labels),
        'source_totals': json.dumps(source_totals),
        'category_labels': json.dumps(category_labels),
        'category_totals': json.dumps(category_totals),
    })


def not_logged_in(user):
    return not user.is_authenticated


@user_passes_test(not_logged_in, login_url='/finance_tracker', redirect_field_name=None)  
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            return redirect(reverse('select_gender')) 
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
    
    gender = UserProfile.objects.filter(user=request.user).values('gender')[0]['gender']

    # Filter and sort income records based on user and month
    user_incomes = Income.objects.filter(
        user=request.user,
        date_received__year=YEAR,
        date_received__month=month_number
    ).order_by('-date_received', '-time_received')

    # Handle the form submission
    if request.method == 'POST':
        form = IncomeForm(request.POST, user=request.user)
        if form.is_valid():
            # Save the form instance but assign the logged-in user
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            return redirect('income', month_name=month_name)
    else:
        form = IncomeForm(user=request.user)

    return render(request, "finance_tracker/income.html", {
        'month': f"{calendar.month_name[month_number]} {YEAR}",
        'incomes': user_incomes,
        'form': form,
        'months': VALID_MONTHS,
        'month_name': month_name,
        'gender': gender
    })


@login_required
def expenses(request, month_name=None):
    # Handle the current month if no month name is provided
    if not month_name:
        month_name = datetime.datetime.now().strftime('%b') 
        
    # Convert the month name to a month number
    month_number = list(calendar.month_abbr).index(month_name.capitalize())
    
    gender = UserProfile.objects.filter(user=request.user).values('gender')[0]['gender']
    
    # Handle the form submission
    if request.method == "POST":
        form = ExpenseForm(request.POST, user=request.user)
        if form.is_valid():
            
            expense = form.save(commit=False)
            expense.user = request.user  
            expense.save()
            return redirect('expenses', month_name=calendar.month_abbr[month_number])  
    else:
        form = ExpenseForm(user=request.user)  

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
        'month_name': month_name,
        'gender': gender
    })


@login_required
def account_settings(request):
    gender = UserProfile.objects.filter(user=request.user).values('gender')[0]['gender']
    return render(request, "finance_tracker/account_settings.html", {'gender': gender})


@login_required
def custom_password_change(request):
    gender = UserProfile.objects.filter(user=request.user).values('gender')[0]['gender']
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return render(request, 'registration/password_change_done.html', {'gender': gender})
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'registration/password_change.html', {'form': form, 'gender': gender})

@receiver(post_save, sender=User)
def create_default_sources_and_categories(sender, instance, created, **kwargs):
    if created:
        # Create default IncomeSource instances
        default_income_sources = ['Salary', 'Freelance', 'Investment', 'Other']
        for source in default_income_sources:
            IncomeSource.objects.create(name=source, user=instance)
        
        # Create default ExpenseCategory instances
        default_expense_categories = ['Groceries', 'Rent', 'Utilities', 'Entertainment', 'Other']
        for category in default_expense_categories:
            ExpenseCategory.objects.create(name=category, user=instance)
            
def select_gender(request):
    if request.method == 'POST':
        form = GenderSelectionForm(request.POST)
        if form.is_valid():
            # Save the gender in the user's profile
            gender = form.cleaned_data['gender']
            UserProfile.objects.create(user=request.user, gender=gender)
            current_month = datetime.datetime.now().strftime('%b')
            return redirect(reverse('index', kwargs={'month_name': current_month}))
    else:
        form = GenderSelectionForm()
    return render(request, 'finance_tracker/select_gender.html', {'form': form})

@login_required
def sources(request, month_name=None):
    # Handle the current month if no month name is provided
    if not month_name:
        month_name = datetime.datetime.now().strftime('%b') 
        
    # Convert the month name to a month number
    month_number = list(calendar.month_abbr).index(month_name.capitalize())
    
    gender = UserProfile.objects.filter(user=request.user).values('gender')[0]['gender']
    
    sources = IncomeSource.objects.filter(user=request.user)
    other_source = IncomeSource.objects.get(user=request.user, name='Other')
    
    sources = list(sources)  # Convert queryset to list (if needed)
    sources.sort(key=lambda source: source.name == "Other") 
    
    # Filter income sources by month
    income_sources = Income.objects.filter(
        user=request.user,
        date_received__year=YEAR,
        date_received__month=month_number
    ).values('source__name').annotate(total=Sum('amount'))
    
    source_labels = [source['source__name'] for source in income_sources]
    source_totals = [float(source['total']) for source in income_sources]
    
    if request.method == 'POST':
        form = IncomeSourceForm(request.POST)
        if form.is_valid():
            source = form.save(commit=False)
            source.user = request.user
            source.save()
            return redirect('sources')
    elif request.method == 'GET' and 'delete' in request.GET:
        item_id = request.GET.get('delete')
        item = get_object_or_404(IncomeSource, id=item_id, user=request.user)
        
         # Prevent deletion of "Other"
        if item.name == 'Other':
            messages.error(request, "You cannot delete the 'Other' source.")
        else:
            # Reassign incomes to "Other"
            Income.objects.filter(source=item).update(source=other_source)
            item.delete()
        return redirect('sources')
    else:
        form = IncomeSourceForm()

    return render(request, 'finance_tracker/sources.html', {
        'form': form,
        'sources': sources,
        'gender': gender,
        'month_name': month_name,
        'months': VALID_MONTHS,
        'source_labels': json.dumps(source_labels),
        'source_totals': json.dumps(source_totals),
        })
    
@login_required
def spendings(request, month_name=None):
    # Handle the current month if no month name is provided
    if not month_name:
        month_name = datetime.datetime.now().strftime('%b') 
        
    # Convert the month name to a month number
    month_number = list(calendar.month_abbr).index(month_name.capitalize())
    
    gender = UserProfile.objects.filter(user=request.user).values('gender')[0]['gender']
    
    categories = ExpenseCategory.objects.filter(user=request.user)
    other_category = ExpenseCategory.objects.get(user=request.user, name='Other')
    
    categories = list(categories)  # Convert queryset to list (if needed)
    categories.sort(key=lambda category: category.name == "Other") 
    
    # Filter income sources by month
    expense_categories = Expense.objects.filter(
        user=request.user,
        date_incurred__year=YEAR,
        date_incurred__month=month_number
    ).values('category__name').annotate(total=Sum('amount'))
    
    category_labels = [category['category__name'] for category in expense_categories]
    category_totals = [float(category['total']) for category in expense_categories]
    
    
    if request.method == 'POST':
        form = ExpenseCategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('spendings')
    elif request.method == 'GET' and 'delete' in request.GET:
        item_id = request.GET.get('delete')
        item = get_object_or_404(ExpenseCategory, id=item_id, user=request.user)
        
         # Prevent deletion of "Other"
        if item.name == 'Other':
            messages.error(request, "You cannot delete the 'Other' source.")
        else:
            # Reassign incomes to "Other"
            Expense.objects.filter(category=item).update(category=other_category)
            item.delete()
        return redirect('spendings')
    else:
        form = ExpenseCategoryForm()

    return render(request, 'finance_tracker/spendings.html', {
        'form': form,
        'categories': categories,
        'gender': gender,
        'month_name': month_name,
        'months': VALID_MONTHS,
        'category_labels': json.dumps(category_labels),
        'category_totals': json.dumps(category_totals),
        })

@user_passes_test(not_logged_in)    
def landing_page(request):
    return render(request, 'finance_tracker/landing_page.html')
