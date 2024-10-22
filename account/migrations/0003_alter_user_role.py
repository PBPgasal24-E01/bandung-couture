# Generated by Django 5.1.2 on 2024-10-22 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_remove_user_status_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Visitor'), (2, 'Contributor')], null=True),
        ),
    ]
