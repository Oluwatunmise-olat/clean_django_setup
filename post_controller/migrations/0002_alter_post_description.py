# Generated by Django 4.0.4 on 2022-05-03 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post_controller', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='description',
            field=models.TextField(null=True),
        ),
    ]
