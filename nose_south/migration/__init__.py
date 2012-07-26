import sys
from django.utils import importlib

from south.migration.base import application_to_app_label
from south.migration.utils import app_label_to_app_module


class AppMigrationMetaclass(type):

    """
    Metaclass which ensures there is only one instance of a AppMigration for
    any given app.
    """

    def __init__(self, name, bases, dict):
        super(AppMigrationMetaclass, self).__init__(name, bases, dict)
        self.instances = {}

    def __call__(self, application, **kwds):

        app_label = application_to_app_label(application)

        # If we don't already have an instance, make one
        if app_label not in self.instances:
            self.instances[app_label] = (
                super(AppMigrationMetaclass, self).__call__(
                    app_label_to_app_module(app_label), **kwds))

        return self.instances[app_label]

    def _clear_cache(self):
        "Clears the cache of Migration objects."
        self.instances = {}


class AppMigrationTest(object):

    __metaclass__ = AppMigrationMetaclass

    def __init__(self, app):
        self._migration_tests = None
        self.application = app
        self.results = []

    @property
    def application(self):
        return self._application

    @application.setter
    def set_application(self, application):
        self._application = application
        if not self._migration_tests:
            try:
                migration_tests = (self._application.__name__ +
                                   '.migrations.migration_tests')
                module = importlib.import_module(migration_tests)
                self._migration_tests = module
            except ImportError:
                pass

    def call_method(self, method_name, is_test, *args, **kwargs):
        try:
            method = getattr(self._migration_tests, method_name)
        except AttributeError:
            pass
        try:
            method(*args, **kwargs)
            result = "PASS"
        except:
            result = sys.exc_info()
        if is_test:
            self.results.append(result)

    def prepareTestLoader(self, loader):
        loader.loadTestsFromGenerator(self.replay_results)

    def replay_results(self):
        "Function for nose"
        def raise_exception(exc_info):
            raise self.exc_info[1], None, self.exc_info[2]

        for result in self.results:
            if result == "PASS":
                yield None
            else:
                yield raise_exception, result

    def ran_migration(self, migration, method):
        self.call_method("test_{0}".format(migration), True, method)

    def pre_migrate(self):
        self.call_method("pre", is_test=False)

    def post_migrate(self):
        self.call_method("post", is_test=False)


