from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

CURRENCY_CHOICES = [
    ("USD", "US Dollar"),
    ("PLN", "Polish Złoty"),
    ("EUR", "Euro"),
    ("GBP", "British Pound"),
]

COLOR_THEMES_CHOICES = [
    ("blue", "Blue"),
    ("pink", "Pink"),
    ("lightBlue", "Light Blue"),
    ("brown", "Brown"),
    ("grey", "Grey"), 
    ("green", "Green")
]

class IncomeSource(models.Model):
    name = models.CharField(max_length=25)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('name', 'user')
        
    def __str__(self):
        return self.name

class ExpenseCategory(models.Model):
    name = models.CharField(max_length=25)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('name', 'user')
        
    def __str__(self):
        return self.name

class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0.01)], null=False, blank=False)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default="USD")
    source = models.ForeignKey(IncomeSource, on_delete=models.CASCADE, null=False)
    date_received = models.DateField(null=False, blank=False)
    time_received = models.TimeField(null=False, blank=False)
    description = models.TextField(null=True, blank=True, max_length=25)
    
    def __str__(self):
        return f"{self.amount} - {self.date_received}"
    
class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0.01)], null=False, blank=False)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default="USD")
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE, null=False)
    date_incurred = models.DateField(null=False, blank=False)
    time_incurred = models.TimeField(null=False, blank=False)
    description = models.TextField(null=True, blank=True, max_length=25)
    
    def __str__(self):
        return f"{self.amount} - {self.date_incurred}"
    
class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='O')
    color_theme = models.CharField(max_length=10, choices=COLOR_THEMES_CHOICES, default="blue")

    preferred_currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default="USD"
    )