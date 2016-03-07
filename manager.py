#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

from app import create_app, db
from app.models import User, Role, Post, Comment

import os

cov = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    cov = coverage.coverage(branch=True, include='app/*')
    cov.start()

app = create_app(os.environ.get('FLASKY_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db,
                User=User, Role=Role, Post=Post, Comment=Comment)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test(coverage=False):
    """Run the unit tests."""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if cov:
        cov.stop()
        cov.save()
        print('Coverage Summary:')
        cov.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        cov.html_report(directory=covdir)
        print('HTML version: file:// % s/index.html' % covdir)
        cov.erase()


@manager.command
def profile(length=25, profile_dir=None):
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length],
                                      profile_dir=profile_dir)
    app.run()


@manager.command
def deploy():
    from flask.ext.migrate import upgrade
    # upgrade database
    upgrade()
    # init role
    Role.init_roles()
    # user follow self
    User.add_self_follows()


if __name__ == '__main__':
    manager.run()
