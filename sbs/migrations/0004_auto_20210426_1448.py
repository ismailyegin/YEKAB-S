# Generated by Django 2.2.6 on 2021-04-26 14:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sbs', '0003_auto_20210416_0957'),
    ]

    operations = [
        migrations.AddField(
            model_name='abirim',
            name='kobilid',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='abirimparametre',
            name='kobilid',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='adosya',
            name='kobilid',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='adosyaparametre',
            name='kobilid',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='aevrak',
            name='kobilid',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='aklasor',
            name='finishyear',
            field=models.IntegerField(blank=True, null=True, verbose_name='finishyear'),
        ),
        migrations.AddField(
            model_name='aklasor',
            name='kobilid',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='aklasor',
            name='startyear',
            field=models.IntegerField(blank=True, null=True, verbose_name='startyear'),
        ),
        migrations.AddField(
            model_name='categoryitem',
            name='kobilid',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='MenuArsiv',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, null=True)),
                ('url', models.CharField(blank=True, max_length=120, null=True)),
                ('is_parent', models.BooleanField(default=True)),
                ('is_show', models.BooleanField(default=True)),
                ('fa_icon', models.CharField(blank=True, max_length=120, null=True)),
                ('sorting', models.IntegerField(blank=True, null=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sbs.MenuArsiv')),
                ('permission', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
