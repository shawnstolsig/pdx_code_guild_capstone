# Generated by Django 3.0.2 on 2020-01-30 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0008_role_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='rate',
            field=models.FloatField(blank=True, null=True),
        ),
    ]