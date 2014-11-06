from fabric.decorators import task, roles
from fabric.state import env
from fabtools import require
import fabtools

__author__ = 'yeongseokjang'

env.roledefs.update({
    'web': ['54.65.59.125'],
})
env.user = 'ubuntu'
env.home = '/home/' + env.user
env.project_name = 'superrocketserver'
env.project_path = env.home + '/' + env.project_name
env.static_path = env.home + '/static'
env.key_filename = 'SuperRocekt-DEV.pem'

@task
@roles('web')
def setup_web():
    require.oracle_jdk.installed(version='8u25-b17')

    require.tomcat.installed(version='8.0.14')
    if not require.service.started():
        require.service.start('tomcat')

    require.nginx.server()
    require.nginx.site(env.project_name, template_source='nginx-superrocket.site',
                       port=80,
                       server_alias='',
                       static_path=env.static_path)
    require.nginx.disable('default')
    require.directory(env.home + '/logs')

def restart_web():
    require.service.restart('tomcat')
    require.service.restart('nginx')