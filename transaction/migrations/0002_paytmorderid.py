# Generated by Django 3.1.4 on 2021-01-10 13:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transaction', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaytmOrderId',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('order_id', models.CharField(max_length=255, unique=True)),
                ('is_used', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('used_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
