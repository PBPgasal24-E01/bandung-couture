# Generated by Django 5.1.2 on 2024-10-19 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promo', '0002_alter_promo_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='promo',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='promo_images/'),
        ),
    ]
