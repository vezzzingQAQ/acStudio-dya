# Generated by Django 3.2.5 on 2021-08-21 01:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('zusers', '0002_user_state'),
        ('zprojects', '0004_auto_20210820_2011'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_head_portrait', models.CharField(default='default.jpg', max_length=50)),
                ('author_name', models.CharField(default='无名氏', max_length=30, verbose_name='用户名')),
                ('good_number', models.IntegerField(default=0)),
                ('content', models.TextField(verbose_name='content')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zprojects.project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zusers.user')),
            ],
        ),
    ]
