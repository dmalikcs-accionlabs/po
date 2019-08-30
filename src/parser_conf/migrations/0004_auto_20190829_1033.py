# Generated by Django 2.2.4 on 2019-08-29 15:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('parser_conf', '0003_auto_20190824_2342'),
    ]

    operations = [
        migrations.AddField(
            model_name='parserconfigurationdef',
            name='share_option',
            field=models.CharField(choices=[('PUB', 'Public'), ('PVT', 'Private'), ('WITH_IN_TEAM', 'With In Team')], default='PVT', max_length=15),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parserconfigurationdef',
            name='user',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
