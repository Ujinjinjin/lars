import glob
import yaml
from cement import Controller, ex
from cement.utils.shell import Prompt
from progress.bar import IncrementalBar

from ..utilities.db_context import DbContext
from ..utilities.parg_validator import PargValidator

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


class Parser(Controller):
    class Meta:
        label = 'parser'
        stacked_type = 'embedded'
        stacked_on = 'base'

    def _default(self):
        """Default action if no sub-command is passed."""
        self.app.args.print_help()

    @ex(
        help='start parsing logs',
        arguments=[
            (['--id', '-i'],
             {'help': 'Application ID',
              'action': 'store',
              'dest': 'id'}),
            (['--name', '-n'],
             {'help': 'Application name',
              'action': 'store',
              'dest': 'name'}),
            (['--path', '-p'],
             {'help': 'Path to logs folder',
              'action': 'store',
              'dest': 'path'}),
        ],
    )
    def parse(self):
        p_id = self.app.pargs.id
        p_name = self.app.pargs.name
        p_path = self.app.pargs.path

        # Validate arguments
        if not PargValidator.single_value(p_id, p_name, p_path):
            self.app.log.error('Log file path is not specified. Please, use parse --help for more information')
            return

        # Specify log file path
        path: str = p_path

        if p_id is not None:
            p_id = int(p_id)
            app = self.app.db.get(doc_id=p_id)

            if app is None:
                self.app.log.warning(f'Application with id {p_id} not found. Use "list" for more info')
                return

            path = app['path']

        if p_name is not None:
            apps = self.app.db.all()
            for app in apps:
                if app['app_name'] == p_name:
                    path = app['path']
                    break

        if path is None:
            self.app.log.error('Log file path could not be specified')

        if path[-1] in ('/', '\\'):
            path = path[:-1]

        # Find .log file
        log_file_names = [f for f in glob.glob(path + '**/*.log', recursive=False)]
        log_file_name: str

        if len(log_file_names) == 0:
            self.app.log.error(f'Not found any .log files in specified path: {path}')
            return
        elif len(log_file_names) == 1:
            log_file_name = log_file_names[0]
        else:
            prompt = Prompt('Chose .log file to parse',
                            options=log_file_names,
                            numbered=True,
                            )
            log_file_name = prompt.input

        self.app.log.info(f'Log file: {log_file_name}')

        # Find 'lars.yml' file
        lars_config_file_names = [f for f in glob.glob(path + '**/lars.yml', recursive=False)]
        if len(lars_config_file_names) == 0:
            self.app.log.error(f'Not found "lars.yml" file in specified path: {path}')
            return
        else:
            lars_config_file_name = lars_config_file_names[0]

        self.app.log.info(f'Config file: {lars_config_file_name}')

        # Read lars config
        with open(lars_config_file_name, 'r', encoding='utf8') as lars_config_file:
            config = yaml.load(lars_config_file, Loader)
            headers = config['headers']
            primary_key = config['primary_key']
            headers_count = len(headers)

            self.app.log.info(f'Headers: {headers}')
            self.app.log.info(f'Primary key: {primary_key}')

        # Read logs from file into array
        with open(log_file_name, 'r', encoding='utf8') as log_file:
            log_array = log_file.read().split('\n')
            logs_count = len(log_array)

            if logs_count == 0:
                self.app.log.warning(f'Log file is empty!')
                return

            self.app.log.info(f'Logs count: {logs_count}')

        # Init database
        db = DbContext(path, headers, primary_key)

        # Init progress bar
        progress_bar = IncrementalBar('Processing: ', max=logs_count)

        # Parse logs to sqlite3
        for i in range(logs_count):
            progress_bar.next()
            log = log_array[i]

            if len(log) == 0:
                continue

            splitted_log = log.split(' | ')
            if len(splitted_log) != headers_count:
                self.app.log.error(f'Column count of some logs does not match headers length!\n'
                                   f'Log: {log}')
                return

            log_dict = dict()
            for j in range(headers_count):
                log_dict[headers[j]] = splitted_log[j]

            if not db.try_insert_log(log_dict):
                self.app.log.error(f'Error inserting log to database')
                return

        # Dispose objects
        progress_bar.finish()
        db.dispose()

        self.app.log.error(f'Finished parsing logs!')