# Generated by Django 4.1.2 on 2022-10-09 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grzyby', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='grzyby',
            name='imageOfShroom',
            field=models.ImageField(default='PIC OR DIDNT HAPPEN', upload_to=''),
        ),
    ]
