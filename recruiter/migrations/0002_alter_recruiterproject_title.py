# Generated by Django 5.0.7 on 2024-08-11 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruiter', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recruiterproject',
            name='title',
            field=models.CharField(max_length=40),
        ),
    ]