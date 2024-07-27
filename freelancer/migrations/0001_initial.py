# Generated by Django 5.0.7 on 2024-07-25 21:29

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FreelancerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(max_length=500)),
                ('active', models.BooleanField(default=True)),
                ('stars', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('image', models.ImageField(blank=True, null=True, upload_to='freelancerIcon/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('desc', models.TextField(max_length=300)),
                ('price', models.FloatField(validators=[django.core.validators.MinValueValidator(5.0)])),
                ('time_in_days', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('revisions', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('image', models.ImageField(blank=True, null=True, upload_to='project_images/')),
                ('fkFler', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='freelancer.freelancerprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Skills',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('fkFler', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='freelancer.freelancerprofile')),
            ],
        ),
    ]
