# Generated by Django 4.0.4 on 2022-05-03 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_controller', '0004_alter_customuser_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
