# Generated by Django 2.2.6 on 2021-04-27 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sbs', '0005_auto_20210426_1454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abirim',
            name='kobilid',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='abirimparametre',
            name='kobilid',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='adosya',
            name='kobilid',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='adosyaparametre',
            name='kobilid',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='aevrak',
            name='kobilid',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='aklasor',
            name='kobilid',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='categoryitem',
            name='kobilid',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
