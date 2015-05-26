# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20150526_1048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(to='user_auth.Student'),
        ),
        migrations.AlterField(
            model_name='rating',
            name='evaluator',
            field=models.ForeignKey(to='user_auth.Student'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(to='user_auth.Student', null=True),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='pub_date',
            field=models.DateTimeField(editable=False, verbose_name='date published'),
        ),
        migrations.DeleteModel(
            name='Person',
        ),
    ]
