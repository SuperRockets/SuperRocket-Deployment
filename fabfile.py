from fabric.decorators import task, roles
from fabric.state import env
from fabtools import require

__author__ = 'yeongseokjang'

env.roledefs.update({
    'web': ['54.65.59.125'],
})
env.user = 'ubuntu'
env.home = '/home/' + env.user
env.project_name = 'superrocketserver'
env.project_path = env.home + '/' + env.project_name
env.static_path = env.home + '/static'
env.key_filename = 'SuperRocket-DEV.pem'

@task
@roles('web')
def setup_web():
    require.nginx.server()
    require.nginx.site(env.project_name, template_source='nginx-superrocket.site',
                       port=80,
                       server_alias='',
                       static_path=env.static_path)
    require.nginx.disable('default')

    require.directory(env.home + '/logs')