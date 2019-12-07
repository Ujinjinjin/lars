import os
from cement import App, TestApp, init_defaults
from cement.core.exc import CaughtSignal
from tinydb import TinyDB
from cement.utils import fs

from .core.exc import LarsError
from .controllers.apps import Apps
from .controllers.base import Base
from .controllers.parser import Parser

# configuration defaults
CONFIG = init_defaults('lars')
CONFIG['lars']['db_file'] = '~/.lars/db.json'


def extend_tinydb(app):
    db_file = app.config.get('lars', 'db_file')

    # ensure that we expand the full path
    db_file = fs.abspath(db_file)

    # ensure our parent directory exists
    db_dir = os.path.dirname(db_file)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    app.extend('db', TinyDB(db_file))


class Lars(App):
    """Lars primary application."""

    class Meta:
        label = 'lars'

        hooks = [
            ('post_setup', extend_tinydb),
        ]

        # configuration defaults
        config_defaults = CONFIG

        # call sys.exit() on close
        exit_on_close = True

        # load additional framework extensions
        extensions = [
            'yaml',
            'colorlog',
            'jinja2',
        ]

        # configuration handler
        config_handler = 'yaml'

        # configuration file suffix
        config_file_suffix = '.yml'

        # set the log handler
        log_handler = 'colorlog'

        # set the output handler
        output_handler = 'jinja2'

        # register handlers
        handlers = [
            Base,
            Parser,
            Apps
        ]


class LarsTest(TestApp, Lars):
    """A sub-class of Lars that is better suited for testing."""

    class Meta:
        label = 'lars'


def main():
    with Lars() as app:
        try:
            app.run()

        except AssertionError as e:
            print('AssertionError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except LarsError as e:
            print('LarsError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except CaughtSignal as e:
            # Default Cement signals are SIGINT and SIGTERM, exit 0 (non-error)
            print('\n%s' % e)
            app.exit_code = 0


if __name__ == '__main__':
    main()
