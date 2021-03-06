# Generated by Django 3.2.6 on 2022-02-26 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0002_medicine'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CUSTOMER_NAME', models.CharField(max_length=500, verbose_name='Customer Name')),
                ('ADDRESS', models.CharField(max_length=500, verbose_name='Adress')),
                ('PRODUCT', models.CharField(max_length=500, verbose_name='Product')),
                ('COST', models.IntegerField(verbose_name='Cost')),
                ('PHONE', models.CharField(max_length=13, verbose_name='Phone Number')),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('EMPLOYEE_NAME', models.CharField(max_length=500, verbose_name='Employee Name')),
                ('ADDRESS', models.CharField(max_length=500, verbose_name='Adress')),
                ('PHONE', models.CharField(max_length=13, verbose_name='phone number')),
                ('USERNAME', models.CharField(max_length=200, verbose_name='Username')),
                ('PASSWORD', models.CharField(max_length=200, verbose_name='Password')),
                ('MEDICINE_SOLD', models.CharField(max_length=500, verbose_name='Medicine Sold')),
                ('SELLING_DATE', models.DateField(verbose_name='Selling Date')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SHELF', models.IntegerField(verbose_name='Shelf Number')),
                ('CLASSIFICATION', models.CharField(max_length=500, verbose_name='classification')),
                ('MEDICINE_NAME', models.CharField(max_length=500, verbose_name='Medicine Name')),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('STORE_NAME', models.CharField(max_length=500, verbose_name='Store Name')),
                ('PLACE', models.CharField(max_length=500, verbose_name='Place')),
                ('MANAGERS_STORE', models.CharField(max_length=500, verbose_name='Manager Store')),
            ],
        ),
    ]
