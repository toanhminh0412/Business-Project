# Generated by Django 4.1.1 on 2022-09-25 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('command_set', '0006_alter_userprofile_saved_command_set'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tool',
            name='title',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
