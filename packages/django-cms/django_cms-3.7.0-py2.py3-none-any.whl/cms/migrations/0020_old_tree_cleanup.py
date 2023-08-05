# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-01-03 19:50
from __future__ import unicode_literals

import django
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion

from . import IrreversibleMigration


class Migration(IrreversibleMigration):

    dependencies = [
        ('cms', '0019_set_pagenode'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='page',
            options={'verbose_name': 'page', 'verbose_name_plural': 'pages', 'permissions': (
            ('view_page', 'Can view page'), ('publish_page', 'Can publish page'),
            ('edit_static_placeholder', 'Can edit static placeholders'))},
        ),
        migrations.AlterField(
            model_name='page',
            name='node',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cms_pages',
                                    to='cms.TreeNode'),
        ),
        migrations.RemoveField(
            model_name='page',
            name='migration_0018_control',
        ),
        migrations.RemoveField(
            model_name='page',
            name='site',
        ),
        migrations.RemoveField(
            model_name='page',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='page',
            name='revision_id',
        ),
        migrations.RemoveField(
            model_name='page',
            name='depth',
        ),
        migrations.RemoveField(
            model_name='page',
            name='numchild',
        ),
        migrations.RemoveField(
            model_name='page',
            name='path',
        ),
    ]

    def apply(self, project_state, schema_editor, collect_sql=False):
        connection = schema_editor.connection
        column_names = [
            column.name for column in
            connection.introspection.get_table_description(connection.cursor(), 'cms_page')
        ]

        if 'migration_0018_control' in column_names:
            # The new 0018 migration has been applied
            return super(Migration, self).apply(project_state, schema_editor, collect_sql)

        # The old 0018 migration was applied
        # Move the project state forward without actually running
        # any of the operations against the database.
        for operation in self.operations:
            operation.state_forwards(self.app_label, project_state)
        return project_state
