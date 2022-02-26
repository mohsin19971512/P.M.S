# Generated by Django 3.2.6 on 2022-02-21 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MEDICINE_NAME', models.CharField(max_length=500, verbose_name='Medicine Name')),
                ('SELLING_PRICE', models.IntegerField(verbose_name='Selling Price')),
                ('EXPIRE_DATE', models.DateField(verbose_name='Expire Date')),
                ('MANUFACTURE_NAME', models.CharField(max_length=500, verbose_name='Manufacture Name')),
                ('UNITARY_PRICE', models.IntegerField(verbose_name='Unitary Price')),
                ('QUANTITY', models.IntegerField(verbose_name='Quantity')),
                ('DISCOUNT', models.IntegerField(verbose_name='Dicount')),
            ],
        ),
    ]
