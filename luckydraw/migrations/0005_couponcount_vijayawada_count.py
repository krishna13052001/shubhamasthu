# Generated by Django 3.2.9 on 2021-12-30 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('luckydraw', '0004_winner'),
    ]

    operations = [
        migrations.AddField(
            model_name='couponcount',
            name='vijayawada_count',
            field=models.IntegerField(default=0),
        ),
    ]