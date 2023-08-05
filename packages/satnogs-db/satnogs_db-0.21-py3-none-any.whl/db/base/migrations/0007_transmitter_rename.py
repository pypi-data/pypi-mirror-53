# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-03-29 19:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


def add_suggestion_permissions(apps, schema_editor):
    pass


def remove_suggestion_permissions(apps, schema_editor):
    """Reverse the above additions of permissions."""
    ContentType = apps.get_model('contenttypes.ContentType')
    Permission = apps.get_model('auth.Permission')
    try:
        content_type = ContentType.objects.get(
            model='suggestion',
            app_label='base',
        )
        # This cascades to Group
        Permission.objects.filter(
            content_type=content_type,
            codename__in=('add_suggestion', 'change_suggestion', 'delete_suggestion'),
        ).delete()
    except ContentType.DoesNotExist:
        pass

class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_auto_20190121_1320'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='suggestion',
            name='transmitter',
        ),
        migrations.RemoveField(
            model_name='suggestion',
            name='citation',
        ),
        migrations.RemoveField(
            model_name='suggestion',
            name='user',
        ),
        migrations.DeleteModel(
            name='Suggestion',
        ),
        migrations.RunPython(remove_suggestion_permissions, add_suggestion_permissions),
        migrations.RenameModel(
            old_name='Transmitter',
            new_name='TransmitterEntry',
        ),
    ]
