# Generated by Django 3.0.8 on 2020-07-27 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_auto_20200727_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empresa',
            name='apelido',
            field=models.CharField(default='empresa', max_length=10),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='nome',
            field=models.CharField(max_length=255),
        ),
    ]
