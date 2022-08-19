# Generated by Django 4.0.6 on 2022-08-11 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('New', 'New'), ('Completed', 'Completed'), ('Accepted', 'Accepted'), ('Cancelled', 'Cancelled')], default='New', max_length=20),
        ),
    ]
