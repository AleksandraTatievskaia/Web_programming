# Generated by Django 5.1.6 on 2025-02-28 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('echo', '0003_alter_book_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('full_name', models.CharField(max_length=255)),
                ('role', models.CharField(choices=[('user', 'User'), ('admin', 'Admin')], default='user', max_length=10)),
            ],
        ),
    ]
