# Generated by Django 3.1.4 on 2020-12-17 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0011_disputedgame'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameresult',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]