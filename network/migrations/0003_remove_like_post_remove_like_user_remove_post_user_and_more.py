# Generated by Django 4.1.1 on 2022-11-28 23:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_user_numberoffollowers_post_like_following'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='post',
        ),
        migrations.RemoveField(
            model_name='like',
            name='user',
        ),
        migrations.RemoveField(
            model_name='post',
            name='user',
        ),
        migrations.RemoveField(
            model_name='user',
            name='numberOfFollowers',
        ),
        migrations.DeleteModel(
            name='Following',
        ),
        migrations.DeleteModel(
            name='Like',
        ),
        migrations.DeleteModel(
            name='Post',
        ),
    ]