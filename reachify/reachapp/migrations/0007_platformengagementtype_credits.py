# Generated by Django 4.2.10 on 2024-02-27 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reachapp', '0006_alter_promotion_end_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='platformengagementtype',
            name='credits',
            field=models.PositiveIntegerField(default=2),
        ),
    ]