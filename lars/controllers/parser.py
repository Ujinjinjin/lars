from cement import Controller, ex


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
            (['--path', '-p'],
             {'help': 'Path to logs folder',
              'action': 'store',
              'dest': 'path'}),
        ],
    )
    def parse(self):
        p_id = self.app.pargs.id
        p_path = self.app.pargs.path

        if (p_id is None and p_path is None) or (p_id is not None and p_path is not None):
            self.app.log.error('Log file path is not specified. Please, use parse --help for more information')
            return

        # config_path = self.app.db.g.
