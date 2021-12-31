# Generated by Django 3.1.2 on 2021-12-31 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('luckydraw', '0005_couponcount_vijayawada_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='winner',
            name='message',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='cards',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='couponcount',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='winner',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]