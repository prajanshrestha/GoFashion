# Generated by Django 3.0.1 on 2021-05-12 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_remove_customer_birthdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='age',
            field=models.IntegerField(null=True),
        ),
    ]
