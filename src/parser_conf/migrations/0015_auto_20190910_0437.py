# Generated by Django 2.2.4 on 2019-09-10 09:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parser_conf', '0014_auto_20190906_0520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postingestion',
            name='parser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_ingestions', to='parser_conf.ParserConfigurationDef'),
        ),
    ]
