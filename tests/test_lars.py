from pytest import raises
from lars.main import LarsTest


def test_lars():
    # test lars without any subcommands or arguments
    with LarsTest() as app:
        app.run()
        assert app.exit_code == 0


def test_lars_debug():
    # test that debug mode is functional
    argv = ['--debug']
    with LarsTest(argv=argv) as app:
        app.run()
        assert app.debug is True


def test_apps_list():
    app_name = 'TestApp'
    app_path = 'SomePath'
    # add app to list
    argv = ['apps', 'add', '-n', app_name, '-p', app_path]
    with LarsTest(argv=argv) as cli:
        cli.run()

    # test apps list without arguments
    argv = ['apps', 'list']
    with LarsTest(argv=argv) as cli:
        cli.run()
        data, output = cli.last_rendered
        assert cli.pargs.extended is False
        assert data is not None, data
        assert len(data['items']) == 1
        app = data['items'][0]
        assert app['app_name'] == app_name
        assert app['path'] == app_path
        assert output.find('Path:') == -1

    # test apps list with arguments
    argv = ['apps', 'list', '-e']
    with LarsTest(argv=argv) as cli:
        cli.run()
        data, output = cli.last_rendered
        assert cli.pargs.extended is True
        assert data is not None, data
        assert len(data['items']) == 1
        app = data['items'][0]
        assert app['app_name'] == app_name
        assert app['path'] == app_path
        assert output.find('Path:') != -1

    # clean
    argv = ['apps', 'remove', '-n', app_name]
    with LarsTest(argv=argv) as cli:
        cli.run()
