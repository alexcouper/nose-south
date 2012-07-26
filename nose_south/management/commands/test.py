from django.core.management.commands import test

from southtests.migration.listener import setup_handlers

# Looks to each app for a migrations directory
# within which, any test folder is found
# and a list of tests found.
#
# Functions are called in this order
# pre_migrate: start_migration_tests
# for each migration in the app:
# test_ran_<name_of_migration>.
# post_migrate: end_migration_tests

class Command(test.Command):
    def handle(self, *args, **kwargs):
        setup_handlers()
        super(Command, self).handle(*args, **kwargs)
