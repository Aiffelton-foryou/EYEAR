# Generated by Django 4.0.4 on 2022-05-18 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchimage',
            name='time',
            field=models.DateTimeField(null=True),
        ),
    ]
