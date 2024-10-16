# Generated by Django 5.1.2 on 2024-10-15 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=31)),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=31)),
                ('description', models.TextField(null=True)),
                ('address', models.TextField()),
                ('contact_number', models.IntegerField()),
                ('website', models.URLField()),
                ('instagram_account', models.CharField(max_length=31)),
                ('category', models.ManyToManyField(to='stores.category')),
            ],
        ),
    ]
