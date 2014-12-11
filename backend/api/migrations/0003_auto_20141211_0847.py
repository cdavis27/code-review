# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import api.models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20141211_0836'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='file',
            field=models.FileField(default='blank', upload_to=api.models.File_file),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='project_file',
            field=models.FileField(null=True, upload_to=api.models.File_file, blank=True),
            preserve_default=True,
        ),
    ]
