# Generated by Django 4.0.3 on 2022-03-16 09:15

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='USer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(default=api.models.generate_unique_code, max_length=50, unique=True)),
                ('username', models.CharField(max_length=20)),
                ('age', models.IntegerField()),
                ('image_path', models.TextField(blank=True, default=' ', null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images')),
                ('Image_flag', models.IntegerField()),
            ],
        ),
    ]
