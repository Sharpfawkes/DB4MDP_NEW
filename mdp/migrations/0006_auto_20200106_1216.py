# Generated by Django 3.0.2 on 2020-01-06 18:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mdp', '0005_auto_20200106_1214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='task_property',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='mdp_props', to='mdp.MDPProps'),
        ),
    ]
