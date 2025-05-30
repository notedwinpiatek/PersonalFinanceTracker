# Generated by Django 5.1.5 on 2025-05-03 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance_tracker', '0004_alter_expensecategory_name_alter_incomesource_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='currency',
            field=models.CharField(choices=[('USD', 'US Dollar'), ('PLN', 'Polish Złoty'), ('EUR', 'Euro'), ('GBP', 'British Pound')], default='USD', max_length=3),
        ),
        migrations.AddField(
            model_name='income',
            name='currency',
            field=models.CharField(choices=[('USD', 'US Dollar'), ('PLN', 'Polish Złoty'), ('EUR', 'Euro'), ('GBP', 'British Pound')], default='USD', max_length=3),
        ),
    ]
