# Generated by Django 2.2.4 on 2019-08-24 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingestion', '0002_auto_20190824_1353'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingestiondata',
            name='status',
            field=models.CharField(choices=[('N', 'NEW'), ('C_F', 'Failed'), ('C_S', 'Completed')], default='N', max_length=2),
        ),
    ]
