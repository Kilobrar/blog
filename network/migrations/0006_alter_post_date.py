# Generated by Django 4.1.1 on 2022-12-23 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_user_numberoffollowed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]