# Generated by Django 5.0.7 on 2024-07-21 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CatalystCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='name')),
                ('domain', models.CharField(max_length=200, verbose_name='domain')),
                ('year_founded', models.CharField(max_length=20, verbose_name='year founded')),
                ('industry', models.CharField(max_length=250, verbose_name='industry')),
                ('locality', models.CharField(blank=True, max_length=250, null=True, verbose_name='locality')),
                ('country', models.CharField(blank=True, max_length=250, null=True, verbose_name='country')),
                ('linkedin_url', models.CharField(blank=True, max_length=250, null=True, verbose_name='linkedin url')),
                ('employees_from', models.CharField(blank=True, max_length=250, null=True, verbose_name='employees_from')),
                ('employees_to', models.CharField(blank=True, max_length=250, null=True, verbose_name='employees_to')),
            ],
        ),
    ]
