from django.conf import settings
from django.utils.importlib import import_module

from south.signals import ran_migration, pre_migrate, post_migrate

from southtests.migration import AppMigrationTest


def callback_ran_migration(app, migration, method):
    AppMigrationTest(app).ran_migration(migration, method)


def callback_pre_migrate(app):
    AppMigrationTest(app).pre_migrate()


def callback_post_migrate(app):
    AppMigrationTest(app).post_migrate()


def setup_handlers():
    ran_migration.connect(callback_ran_migration)
    pre_migrate.connect(callback_pre_migrate)
    post_migrate.connect(callback_post_migrate)
