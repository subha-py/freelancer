from fabric.contrib.files import append,exists,sed
from fabric.api import env,local,run
import random

REPO_URL='https://github.com/subha-py/freelancer'

def deploy():
    site_folder='/home/%s/sites/%s' % (env.user,env.host)
    source_folder=site_folder+'/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder,env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)

def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database','static','virtualenv','source'):
        run('mkdir -p %s/%s'%(site_folder,subfolder))

def _get_latest_source(source_folder):
    if exists(source_folder+'/.git'):
        run('cd %s && git fetch' % (source_folder,))
        #git fetch inside an existing repository pulls down all the latest commits from the Web.
    else:
        run('git clone %s %s'%(REPO_URL,source_folder))
        #Alternatively we use git clone with the repo URL to bring down a fresh source tree.
    current_commit=local('git log -n 1 --format=%H',capture=True)
    # Fabric's local command works in your local machine it is just a wrapper around subporocess.Popen
    #here we capture the log from the git site
    run('cd %s && git reset --hard %s'%(source_folder,current_commit))
    #we use --hard to delete any pending git task in server
    #use a push if you come up with any error

def _update_settings(source_folder,site_name):
    settings_path=source_folder + '/freelancer/settings.py'
    sed(settings_path,'DEBUG = True','DEBUG = False')
    sed(settings_path,
        'ALLOWED_HOSTS =.+$',
        'ALLOWED_HOSTS= ["%s"]'%(site_name,)
        )
    secret_key_file=source_folder+'/freelancer/secret_key.py'
    if not exists(secret_key_file):
        chars='abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key=''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file,'SECRET_KEY = "%s" '%(key))
    append(settings_path,'\nfrom .secret_key import SECRET_KEY')

def _update_virtualenv(source_folder):
    virtualenv_folder=source_folder+'/../virtualenv'
    if not exists(virtualenv_folder+'/bin/pip'):
        run('virtualenv --python=python27 %s'%(virtualenv_folder))
    run('%s/bin/pip install -r %s/requirements.txt'%(virtualenv_folder,source_folder))

def _update_static_files(source_folder):
    run('cd %s && ../virtualenv/bin/python manage.py collectstatic --noinput'%(source_folder))

def _update_database(source_folder):
    run('cd %s && ../virtualenv/bin/python manage.py migrate --noinput '%(source_folder))