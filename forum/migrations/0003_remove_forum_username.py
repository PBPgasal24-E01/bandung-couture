# Generated by Django 5.1.2 on 2024-10-17 06:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_forum_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='forum',
            name='username',
        ),
    ]
