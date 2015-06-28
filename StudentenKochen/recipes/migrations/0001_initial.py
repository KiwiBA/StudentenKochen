# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('comment', models.CharField(max_length=2000)),
                ('author', models.ForeignKey(to='user_auth.Student')),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('rating', models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=3)),
                ('evaluator', models.ForeignKey(to='user_auth.Student')),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('recipename', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(editable=False, verbose_name='date published')),
                ('description', models.CharField(max_length=20000)),
                ('author', models.ForeignKey(to='user_auth.Student', null=True)),
                ('ingredients', models.ManyToManyField(to='recipes.Ingredient')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('tagname', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(to='recipes.Tag'),
        ),
        migrations.AddField(
            model_name='rating',
            name='recipe',
            field=models.ForeignKey(to='recipes.Recipe'),
        ),
        migrations.AddField(
            model_name='comment',
            name='recipe',
            field=models.ForeignKey(to='recipes.Recipe'),
        ),
    ]
