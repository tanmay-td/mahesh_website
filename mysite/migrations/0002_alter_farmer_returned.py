# Generated by Django 3.2.9 on 2021-11-18 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farmer',
            name='returned',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10),
        ),
    ]
