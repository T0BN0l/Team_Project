# Generated by Django 2.1.5 on 2021-08-03 17:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0007_auto_20210803_1829'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userlikes',
            old_name='title',
            new_name='liked_title',
        ),
    ]
