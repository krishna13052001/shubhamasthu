# Generated by Django 3.1.2 on 2021-12-31 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('luckydraw', '0006_auto_20211231_1317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='winner',
            name='message',
            field=models.CharField(default='Hello', max_length=500),
        ),
    ]