# Generated by Django 3.2.9 on 2021-11-19 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0005_alter_farmer_returned'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agent',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='farmer',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]