# Generated by Django 3.0.2 on 2020-01-28 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0002_auto_20200125_1229'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='color',
            field=models.CharField(default='#FFFFFF', max_length=50),
        ),
        migrations.AddField(
            model_name='node',
            name='height',
            field=models.IntegerField(default=100),
        ),
        migrations.AddField(
            model_name='node',
            name='width',
            field=models.IntegerField(default=200),
        ),
        migrations.AddField(
            model_name='node',
            name='x',
            field=models.IntegerField(default=100),
        ),
        migrations.AddField(
            model_name='node',
            name='y',
            field=models.IntegerField(default=100),
        ),
        migrations.AddField(
            model_name='zone',
            name='color',
            field=models.CharField(default='#FFFFFF', max_length=50),
        ),
        migrations.AddField(
            model_name='zone',
            name='height',
            field=models.IntegerField(default=500),
        ),
        migrations.AddField(
            model_name='zone',
            name='width',
            field=models.IntegerField(default=500),
        ),
        migrations.AddField(
            model_name='zone',
            name='x',
            field=models.IntegerField(default=100),
        ),
        migrations.AddField(
            model_name='zone',
            name='y',
            field=models.IntegerField(default=100),
        ),
    ]
