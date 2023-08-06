import platform
import subprocess

from ccmlib import extension


def java_home_env_hook(node, env):
    system = platform.system()

    if system == 'Darwin':
        env['JAVA_HOME'] = subprocess.check_output(['/usr/libexec/java_home', '-v', '1.8']).decode('utf-8').strip()

    # TODO: implement other platform support here

    else:
        raise Exception('Automatic Java 1.8 environment configuration not available for this platform.')


def register_extensions():
    extension.APPEND_TO_SERVER_ENV_HOOKS.append(java_home_env_hook)