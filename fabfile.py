import os
from fabric.contrib.files import sed
from fabric.api import env, local, run
from fabric.api import env


abs_dir_path = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))

env.user = '#'
env.hosts = ['#']
env.password = '#'
env.full_name_user = '#'
env.user_group = '#'
env.user_name = '#'
env.ssh_keys_dir = os.path.join(abs_dir_path, '#')

def start_provision():
    env.ssh_keys_name = os.path.join(
        env.ssh_keys_dir, env.host_string + '_prod_key')
    local('ssh-keygen -t rsa -b 2048 -f {0}'.format(env.ssh_keys_name))
    local('cp {0} {1}/authorized_keys'.format(
        env.ssh_keys_name + '.pub', env.ssh_keys_dir))
    sed('/etc/ssh/sshd_config', '^UsePAM yes', 'UsePAM no')
    sed('/etc/ssh/sshd_config', '^PermitRootLogin yes',
        'PermitRootLogin no')
    sed('/etc/ssh/sshd_config', '^#PasswordAuthentication yes',
        'PasswordAuthentication no')

    install_ansible_dependencies()
    create_deployer_group()
    create_deployer_user()
    upload_keys()
    set_selinux_permissive()
    run('service sshd reload')
    upgrade_server()