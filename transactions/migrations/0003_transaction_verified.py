# Generated by Django 2.1.3 on 2018-12-18 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_auto_20181204_1345'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='verified',
            field=models.BooleanField(default=False),
        ),
    ]
