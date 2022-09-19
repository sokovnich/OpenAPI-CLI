import subprocess
from setuptools import setup, find_packages
import shutil
import os
from distutils.cmd import Command


project_dir = os.path.dirname(__file__)

with open(os.path.join(project_dir, 'README.md')) as readme:
    long_description = readme.read()

with open(os.path.join(project_dir, 'requirements.txt')) as requirements:
    install_requirements = requirements.read().split('\n')

with open(os.path.join(project_dir, 'test-requirements.txt')) as requirements:
    test_requirements = requirements.read().split('\n')


class InstallBashCompletion(Command):
    description = 'Install bash-completion support'
    user_options = []
    script_path = './openapi_cli_completion.bash'

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        dst_path = os.path.join(os.path.expanduser('~'), '.bash_completion')
        print('Installing bash-completion script to {}'.format(dst_path))
        try:
            shutil.copy(self.script_path, dst_path)
        except IOError as e:
            if e.errno == 13:
                print('Installation failed. Maybe you need to run command with sudo access?')
            raise e

        print('Installation succeeded. You need reload your shell to enable completion.')


setup(
    name='openapi-cli',
    version='0.0.1',
    python_requires='>=2.7',
    packages=find_packages(exclude=['*.tests', 'tests.*', 'tests', '*.tests.*']),
    author='Sokovnich Yan',
    author_email='x6@live.ru',
    url='https://github.com/sokovnich/OpenAPI-CLI',
    long_description=long_description,
    install_requires=install_requirements,
    tests_require=test_requirements,
    test_suite='openapi_cli.tests',
    entry_points={
        'console_scripts': [
            'openapi-cli = openapi_cli.main:main',
        ],
    },
    cmdclass={
        'install_bash_completion': InstallBashCompletion,
    },
)
