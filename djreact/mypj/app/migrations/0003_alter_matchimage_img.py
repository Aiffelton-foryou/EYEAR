# Generated by Django 4.0.4 on 2022-05-18 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_matchimage_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchimage',
            name='img',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]