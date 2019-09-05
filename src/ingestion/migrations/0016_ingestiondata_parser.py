# Generated by Django 2.2.4 on 2019-09-04 07:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parser_conf', '0010_auto_20190829_2354'),
        ('ingestion', '0015_ingestiondataattachment_headers'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingestiondata',
            name='parser',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, to='parser_conf.ParserConfigurationDef'),
        ),
    ]
