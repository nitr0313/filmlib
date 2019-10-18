# Generated by Django 2.2.6 on 2019-10-17 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filmlib', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='rait_out',
        ),
        migrations.AddField(
            model_name='movie',
            name='duration',
            field=models.CharField(default='00:00:00', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='kinopoisk_id',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='movie',
            name='rait_home',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='slug',
            field=models.SlugField(default=''),
        ),
        migrations.AlterField(
            model_name='movie',
            name='about',
            field=models.CharField(blank=True, default='', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='add_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='director',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='genre',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='poster',
            field=models.URLField(default='', null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='rait',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='release',
            field=models.IntegerField(blank=True, default=1900, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='stars',
            field=models.CharField(blank=True, default='', max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='title',
            field=models.CharField(db_index=True, max_length=50),
        ),
    ]