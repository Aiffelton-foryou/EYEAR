# Generated by Django 4.0.4 on 2022-05-26 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_matchimage_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='matchimage',
            name='img',
        ),
        migrations.RemoveField(
            model_name='matchimage',
            name='time',
        ),
        migrations.AddField(
            model_name='matchimage',
            name='content',
            field=models.TextField(null=True),
        ),
    ]
