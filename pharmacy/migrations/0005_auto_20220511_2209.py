# Generated by Django 3.2.6 on 2022-05-11 19:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0004_auto_20220226_2059'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pharmacyclerk',
            name='admin',
        ),
        migrations.DeleteModel(
            name='Doctor',
        ),
        migrations.DeleteModel(
            name='PharmacyClerk',
        ),
    ]
