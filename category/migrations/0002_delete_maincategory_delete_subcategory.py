# Generated by Django 4.0.6 on 2022-08-13 04:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MainCategory',
        ),
        migrations.DeleteModel(
            name='SubCategory',
        ),
    ]