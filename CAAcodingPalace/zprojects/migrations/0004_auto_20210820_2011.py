# Generated by Django 3.2.5 on 2021-08-20 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zprojects', '0003_project_author_head_portrait'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='author_name',
            field=models.CharField(default='无名氏', max_length=30, verbose_name='用户名'),
        ),
        migrations.AddField(
            model_name='project',
            name='good_number',
            field=models.IntegerField(default=0),
        ),
    ]
