# Generated by Django 2.2.1 on 2020-03-10 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='mobile',
            field=models.BigIntegerField(blank=True, null=True, unique=True),
        ),
    ]
