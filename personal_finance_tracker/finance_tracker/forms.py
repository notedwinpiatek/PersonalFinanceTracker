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
        widgets = {
            'date_received': forms.DateInput(attrs={'type': 'date'}),
            'time_received': forms.TimeInput(attrs={'type': 'time'}),
            'describtion': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }