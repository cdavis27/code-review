# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20141211_0942'),
    ]

    operations = [
        migrations.AddField(
            model_name='language',
            name='codemirror_mode',
            field=models.CharField(default='python', max_length=100),
            preserve_default=False,
        ),
    ]
