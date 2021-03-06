# Generated by Django 3.2.5 on 2021-08-20 05:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('zusers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='新建项目', max_length=50)),
                ('introduction', models.TextField(verbose_name='介绍')),
                ('code', models.TextField(verbose_name='code')),
                ('type', models.CharField(default='processing.py', max_length=50)),
                ('cover_portrait', models.CharField(default='defaultCover.jpg', max_length=50)),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zusers.user')),
            ],
        ),
    ]
