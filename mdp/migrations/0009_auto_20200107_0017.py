# Generated by Django 3.0.2 on 2020-01-07 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mdp', '0008_auto_20200107_0011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qualitymeasure',
            name='best',
            field=models.IntegerField(),
        ),
    ]
