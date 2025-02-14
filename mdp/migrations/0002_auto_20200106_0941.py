# Generated by Django 3.0.2 on 2020-01-06 15:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mdp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='variants',
            options={'verbose_name_plural': 'Variants'},
        ),
        migrations.AlterField(
            model_name='mathjaxformulas',
            name='equation_type',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='eqntype', to='mdp.EqnTypes'),
        ),
    ]
