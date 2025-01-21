from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


# Create your models here.
class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0.01)], null=False, blank=False)
    source = models.CharField(max_length=255, null=False, blank=False)
    date_received = models.DateField(null=False, blank=False)
    time_received = models.TimeField(null=False, blank=False)
    describtion = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.amount} - {self.date_received}"
    
class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0.01)], null=False, blank=False)
    category = models.CharField(max_length=255, null=False, blank=False)
    date_incurred = models.DateField(null=False, blank=False)
    time_incurred = models.TimeField(null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    
    def __srt__(self):
        return f"{self.amount} - {self.date_incurred}"
    
class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='O')