# Generated by Django 2.0.1 on 2018-01-02 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0002_blog_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='summary',
            field=models.TextField(max_length=150),
        ),
    ]