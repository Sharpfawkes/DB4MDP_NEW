# Generated by Django 3.0.2 on 2020-01-07 13:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mdp', '0012_auto_20200107_0749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='reference_list',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mdp.Reference'),
        ),
    ]
