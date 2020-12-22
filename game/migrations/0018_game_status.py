# Generated by Django 3.1.4 on 2020-12-22 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0017_game_room_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='status',
            field=models.CharField(choices=[('CREATED', 'CREATED'), ('RUNNING', 'RUNNING'), ('WAITING', 'WAITING'), ('OVER', 'OVER')], default='CREATED', max_length=100),
        ),
    ]