# Generated by Django 3.0.2 on 2020-01-24 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0003_auto_20200121_2049'),
    ]

    operations = [
        migrations.AddField(
            model_name='manager',
            name='darkModeEnabled',
            field=models.BooleanField(default=False),
        ),
    ]