# Generated by Django 4.2.10 on 2024-02-17 23:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reachapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socialprofile',
            name='platform',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='reachapp.platform'),
        ),
    ]
