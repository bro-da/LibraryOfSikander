# Generated by Django 4.0.6 on 2022-08-19 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0015_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Cancelled', 'Cancelled'), ('Completed', 'Completed'), ('New', 'New'), ('Accepted', 'Accepted')], default='New', max_length=20),
        ),
    ]
