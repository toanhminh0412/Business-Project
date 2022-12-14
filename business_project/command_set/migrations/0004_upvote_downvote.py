# Generated by Django 4.1.1 on 2022-09-21 04:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('command_set', '0003_remove_commandset_downvote_num'),
    ]

    operations = [
        migrations.CreateModel(
            name='Upvote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('command_set', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='command_set.commandset')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'command_set_upvote',
                'ordering': ['user'],
            },
        ),
        migrations.CreateModel(
            name='Downvote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('command_set', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='command_set.commandset')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'command_set_downvote',
                'ordering': ['user'],
            },
        ),
    ]
