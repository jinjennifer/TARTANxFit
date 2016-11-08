# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-02 03:49
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('TxFApp', '0005_classattendance_attended'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='classattendance',
            unique_together=set([('user', 'course')]),
        ),
    ]