# Generated by Django 3.0.5 on 2020-07-20 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20200720_0044'),
    ]

    operations = [
        migrations.AddField(
            model_name='platformuser',
            name='goal',
            field=models.TextField(default='None'),
        ),
        migrations.AddField(
            model_name='platformuser',
            name='submitedGoal',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
