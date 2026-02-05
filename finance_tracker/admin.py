from django.contrib import admin
from .models import Income, Expense, UserProfile, IncomeSource, ExpenseCategory

# Register your models here.
admin.site.register(Income)
admin.site.register(Expense)
admin.site.register(UserProfile)
admin.site.register(IncomeSource)
admin.site.register(ExpenseCategory)