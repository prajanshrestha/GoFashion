# Generated by Django 3.1.6 on 2021-02-23 10:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_order_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='status',
            new_name='order_completed',
        ),
    ]
