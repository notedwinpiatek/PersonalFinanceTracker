from django import forms
from .models import Income
from django.contrib.auth.forms import PasswordChangeForm

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'placeholder': 'Current Password', 'class': 'form-control'})
        self.fields['new_password1'].widget.attrs.update({'placeholder': 'New Password', 'class': 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'placeholder': 'Confirm New Password', 'class': 'form-control'})

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['amount', 'source', 'date_received', 'time_received', 'describtion']
        labels = {
            'amount': '',
            'source': '',
            'date_received': '',
            'time_received': '',
            'describtion': '',
        }
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'id': 'amount-field', 'placeholder':'Amount'}),
            'source': forms.TextInput(attrs={'class': 'form-control', 'id': 'source-field', 'placeholder': 'Source'}),
            'date_received': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time_received': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'describtion': forms.Textarea(attrs={'class': 'form-control', 'id': 'description-field', 'placeholder': 'Add a brief description (optional)', 'rows': 4}),
        }
