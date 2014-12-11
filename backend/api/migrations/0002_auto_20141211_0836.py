# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('line_number', models.IntegerField(default=1)),
                ('text', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('commentor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ReviewRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_reviewed', models.BooleanField(default=False)),
                ('is_read', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_completed', models.DateTimeField(null=True, blank=True)),
                ('project', models.ForeignKey(to='api.Project')),
                ('reviewer', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='file',
            name='language',
            field=models.ForeignKey(to='api.Language'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='file',
            name='project',
            field=models.ForeignKey(to='api.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='file',
            field=models.ForeignKey(to='api.File'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 11, 8, 35, 58, 125735, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='last_edit',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 11, 8, 36, 2, 997470, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='owner',
            field=models.ForeignKey(related_name='my_projects', default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='reviewers',
            field=models.ManyToManyField(related_name='projects_to_review', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
