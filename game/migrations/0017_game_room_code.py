# Generated by Django 3.1.4 on 2020-12-22 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0016_auto_20201222_1415'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='room_code',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
