# Generated by Django 2.1.5 on 2021-08-04 12:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rango', '0004_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check', models.CharField(max_length=128, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserView',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check', models.CharField(max_length=128, unique=True)),
            ],
            options={
                'verbose_name_plural': 'user views',
            },
        ),
        migrations.AddField(
            model_name='category',
            name='description',
            field=models.CharField(default='', max_length=512),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='thumbnail',
            field=models.ImageField(blank=True, upload_to='category_images'),
        ),
        migrations.AddField(
            model_name='page',
            name='description',
            field=models.CharField(default=' ', max_length=512),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='page',
            name='thumbnail',
            field=models.ImageField(blank=True, upload_to='page_images'),
        ),
        migrations.AddField(
            model_name='userview',
            name='page',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='rango.Page'),
        ),
        migrations.AddField(
            model_name='userview',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userlike',
            name='category',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='rango.Category'),
        ),
        migrations.AddField(
            model_name='userlike',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
