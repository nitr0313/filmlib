# Generated by Django 2.2.6 on 2019-10-17 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filmlib', '0002_auto_20191017_2332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='kinopoisk_id',
            field=models.IntegerField(blank=True, db_index=True, default=0),
        ),
    ]