# Generated by Django 3.0.2 on 2020-02-04 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('org', '0005_auto_20200128_1545'),
    ]

    operations = [
        migrations.AddField(
            model_name='cohort',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]