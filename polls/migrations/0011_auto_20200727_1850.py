# Generated by Django 3.0.8 on 2020-07-27 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0010_carteira'),
    ]

    operations = [
        migrations.CreateModel(
            name='Faturamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField(verbose_name='date published')),
                ('idempresa', models.CharField(max_length=10)),
                ('faturamento', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Minuta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField(verbose_name='date published')),
                ('idempresa', models.CharField(max_length=10)),
                ('minuta', models.IntegerField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='carteira',
            name='faturamento',
        ),
        migrations.RemoveField(
            model_name='carteira',
            name='minuta',
        ),
    ]