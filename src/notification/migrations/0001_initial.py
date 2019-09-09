# Generated by Django 2.2.4 on 2019-09-04 05:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='TextNotification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference_object_id', models.CharField(max_length=36, null=True)),
                ('object_id', models.CharField(max_length=36)),
                ('cnt_code', models.IntegerField(default='001', editable=False)),
                ('contact_number', models.IntegerField()),
                ('msg', models.TextField()),
                ('is_dispatched', models.BooleanField()),
                ('is_delivered', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(null=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('reference_content_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reference', to='contenttypes.ContentType')),
            ],
        ),
    ]