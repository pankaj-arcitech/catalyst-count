# Generated by Django 5.0.7 on 2024-09-29 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_uploadedfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalystcount',
            name='country',
            field=models.CharField(blank=True, db_index=True, max_length=250, null=True, verbose_name='country'),
        ),
        migrations.AlterField(
            model_name='catalystcount',
            name='employees_from',
            field=models.CharField(blank=True, db_index=True, max_length=250, null=True, verbose_name='employees_from'),
        ),
        migrations.AlterField(
            model_name='catalystcount',
            name='employees_to',
            field=models.CharField(blank=True, db_index=True, max_length=250, null=True, verbose_name='employees_to'),
        ),
        migrations.AlterField(
            model_name='catalystcount',
            name='industry',
            field=models.CharField(db_index=True, max_length=250, verbose_name='industry'),
        ),
        migrations.AlterField(
            model_name='catalystcount',
            name='locality',
            field=models.CharField(blank=True, db_index=True, max_length=250, null=True, verbose_name='locality'),
        ),
        migrations.AlterField(
            model_name='catalystcount',
            name='name',
            field=models.CharField(db_index=True, max_length=250, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='catalystcount',
            name='year_founded',
            field=models.CharField(db_index=True, max_length=20, verbose_name='year founded'),
        ),
    ]
