# Generated by Django 3.0.2 on 2020-01-06 17:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mdp', '0002_auto_20200106_0941'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='languages',
            name='reference_list',
        ),
    ]
