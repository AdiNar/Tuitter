# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-06-15 10:33
from __future__ import unicode_literals

from django.db import migrations, models
from django.db.models.functions import Length


def set_text_length(apps, schema_editor):
    Twit = apps.get_model("twits", "Twit")
    Twit.objects.update(text_length=Length('text'))


class Migration(migrations.Migration):
    """Custom migration adding text-length field to model.
    """

    dependencies = [
        ('twits', '0003_friend'),
    ]

    operations = [
        migrations.AddField(
            model_name='Twit',
            name='text_length',
            field=models.IntegerField(default=0)
        ),
        migrations.RunPython(set_text_length)
    ]
