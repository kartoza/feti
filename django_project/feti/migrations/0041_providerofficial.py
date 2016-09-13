# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('feti', '0040_auto_20160906_0655'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProviderOfficial',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('provider', models.ManyToManyField(to='feti.Provider', verbose_name='Primary Institution')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Primary Institution Official',
            },
        ),
    ]
