from cement import Controller, ex
from ..utilities.parg_validator import PargValidator


class Apps(Controller):
    class Meta:
        label = 'apps'
        help = 'manage your application list'
        stacked_type = 'nested'
        stacked_on = 'base'

    def _default(self):
        """Default action if no sub-command is passed."""
        self.app.args.print_help()

    @ex(
        help='show list applications',
        arguments=[
            (['--extended', '-e'],
             {'help': 'Flag to show extended application info',
              'action': 'store_true',
              'dest': 'extended'}),
        ],
    )
    def list(self):
        p_extended = self.app.pargs.extended

        data = dict()
        data['items'] = self.app.db.all()

        if len(data['items']) == 0:
            self.app.render(data, 'apps/list_empty.jinja2')
            return

        if p_extended:
            self.app.render(data, 'apps/list_extended.jinja2')
        else:
            self.app.render(data, 'apps/list.jinja2')

    @ex(
        help='add application path',
        arguments=[
            (['--name', '-n'],
             {'help': 'Application name',
              'action': 'store',
              'dest': 'name'}),
            (['--path', '-p'],
             {'help': 'Application logfile path',
              'action': 'store',
              'dest': 'path'}),
        ],
    )
    def add(self):
        p_name = self.app.pargs.name
        p_path = self.app.pargs.path

        if p_name is None:
            self.app.log.error('Application name is not specified. Use --help for more information')
            return

        if p_path is None:
            self.app.log.error('Application logfile path is not specified. Use --help for more information')
            return

        apps = self.app.db.all()
        for app in apps:
            if app['app_name'] == p_name:
                self.app.log.error(f'Application {p_name} already exists in storage! Use "list" for more info')
                return
            if app['path'] == p_path:
                self.app.log.error(f'Application {app["app_name"]} has same logfile path! Use "list" for more info')
                return

        item = {
            'app_name': p_name,
            'path': p_path
        }

        self.app.db.insert(item)

    @ex(
        help='remove application from list',
        arguments=[
            (['--id', '-i'],
             {'help': 'Application ID',
              'action': 'store',
              'dest': 'id'}),
            (['--name', '-n'],
             {'help': 'Application name',
              'action': 'store',
              'dest': 'name'}),
        ],
    )
    def remove(self):
        p_id = self.app.pargs.id
        p_name = self.app.pargs.name

        if not PargValidator.single_value(p_id, p_name):
            self.app.log.error('Not specified application to remove. Please, use --help for more information')
            return

        if p_id is not None:
            p_id = int(p_id)
            app = self.app.db.get(doc_id=p_id)

            if app is None:
                self.app.log.warning(f'Application with id {p_id} not found. Use "list" for more info')
                return

            self.app.log.info(f'Removing {app["app_name"]} from application list')
            self.app.db.remove(doc_ids=[p_id])
            return

        if p_name is not None:
            apps = self.app.db.all()
            for app in apps:
                if app['app_name'] == p_name:
                    self.app.log.info(f'Removing {p_name} from application list')
                    self.app.db.remove(doc_ids=[app['doc_id']])
                    return

            self.app.log.warning(f'Application {p_name} not found')
            return
