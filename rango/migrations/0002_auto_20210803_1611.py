# Generated by Django 2.1.5 on 2021-08-03 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='thumbnail',
            field=models.ImageField(blank=True, upload_to='category_images'),
        ),
        migrations.AddField(
            model_name='page',
            name='thumbnail',
            field=models.ImageField(blank=True, upload_to='page_images'),
        ),
    ]