# Generated by Django 3.1 on 2021-11-26 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20211126_1259'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='genre',
        ),
        migrations.AddField(
            model_name='movie',
            name='genre',
            field=models.ManyToManyField(to='main.Genre'),
        ),
    ]
