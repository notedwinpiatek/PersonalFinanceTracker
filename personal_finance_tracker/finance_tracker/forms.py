from django import forms
from .models import Income, Expense, IncomeSource, ExpenseCategory, UserProfile
from django.contrib.auth.forms import PasswordChangeForm

class GenderSelectionForm(forms.Form):
    gender = forms.ChoiceField(
        choices=UserProfile.GENDER_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'gender-select'}),
        label="",
    )
    
class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'placeholder': 'Current Password', 'class': 'form-control'})
        self.fields['new_password1'].widget.attrs.update({'placeholder': 'New Password', 'class': 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'placeholder': 'Confirm New Password', 'class': 'form-control'})

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['amount', 'source', 'date_received', 'time_received', 'description']
        labels = {
            'amount': '',
            'source': '',
            'date_received': '',
            'time_received': '',
            'description': '',
        }
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'id': 'amount-field', 'placeholder':'Amount'}),
            'source': forms.Select(attrs={'class': 'form-control', 'id': 'source-field'}),
            'date_received': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time_received': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'id': 'description-field', 'placeholder': 'Add a brief description (optional)', 'rows': 4}),
        }
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user') 
        super().__init__(*args, **kwargs)
        self.fields['source'].queryset = IncomeSource.objects.filter(user=user)
        
        self.fields['source'].queryset = IncomeSource.objects.filter(user=user)
        self.fields['source'].empty_label = "Source"
        
class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'category', 'date_incurred', 'time_incurred', 'description']
        labels = {
            'amount': '',
            'category': '',
            'date_incurred': '',
            'time_incurred': '',
            'description': '',
        }
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'id': 'amount-field', 'placeholder': 'Amount'}),
            'category': forms.Select(attrs={'class': 'form-control', 'id': 'category-field'}),
            'date_incurred': forms.TextInput(attrs={'type': 'date', 'class': 'form-control', 'id': 'dateInput', 'readonly': 'readonly', 'placeholder': 'mm/dd/yyyy'}), 
            'time_incurred': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}), 
            'description': forms.Textarea(attrs={'class': 'form-control', 'id': 'description-field', 'placeholder': 'Add a brief description (optional)', 'rows': 4}),
        }
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')  # Expect user to be passed to the form
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = ExpenseCategory.objects.filter(user=user)
        
        self.fields['category'].queryset = ExpenseCategory.objects.filter(user=user)
        self.fields['category'].empty_label = "Category"
        
class IncomeSourceForm(forms.ModelForm):
    class Meta:
        model = IncomeSource
        fields = ['name']
        labels = {
            'name': ''
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'New Source'}),
        }

class ExpenseCategoryForm(forms.ModelForm):
    class Meta:
        model = ExpenseCategory
        fields = ['name']
        labels = {
            'name': ''
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'New Category'}),
        }
