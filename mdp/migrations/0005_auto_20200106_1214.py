# Generated by Django 3.0.2 on 2020-01-06 18:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mdp', '0004_auto_20200106_1211'),
    ]

    operations = [
        migrations.CreateModel(
            name='MDPProps',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mdp_property', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='task',
            name='task_property',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mdp_props', to='mdp.MDPProps'),
        ),
    ]
