# Generated by Django 3.0.5 on 2020-07-22 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20200722_1825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estadisticas',
            name='id',
            field=models.TextField(default='0', primary_key=True, serialize=False, unique=True),
        ),
    ]
