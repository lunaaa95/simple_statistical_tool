# Generated by Django 3.0.1 on 2020-01-09 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prob', models.CharField(max_length=300)),
                ('ansr', models.CharField(max_length=300)),
            ],
        ),
    ]