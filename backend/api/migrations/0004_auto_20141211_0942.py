# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20141211_0847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='language',
            field=models.ForeignKey(blank=True, to='api.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='file',
            name='project',
            field=models.ForeignKey(related_name='files', to='api.Project'),
            preserve_default=True,
        ),
    ]
