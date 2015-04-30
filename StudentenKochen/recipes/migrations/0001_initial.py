# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('receptname', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('description', models.CharField(max_length=20000)),
            ],
        ),
        migrations.CreateModel(
            name='Recipeingredients',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('quantity', models.CharField(max_length=30)),
                ('ingredient', models.ForeignKey(to='recipes.Ingredient')),
                ('recipes', models.ForeignKey(to='recipes.Recipe')),
            ],
        ),
        migrations.AddField(
            model_name='recipes',
            name='ingredients',
            field=models.ManyToManyField(to='recipes.Ingredient', through='recipes.Recipeingredients'),
        ),
    ]
