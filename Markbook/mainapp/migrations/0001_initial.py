# Generated by Django 4.2.7 on 2023-12-08 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=20)),
                ('secondname', models.CharField(max_length=20)),
                ('thirdname', models.CharField(max_length=20)),
                ('code', models.CharField(max_length=6, unique=True)),
            ],
        ),
    ]
