from setuptools import setup, find_packages
from sys import platform
from setuptools.command.install import install
import os

with open('requirements.txt', 'r') as req_fp:
    required_packages = req_fp.readlines()

# Use README for long description
with open('README.md', 'r') as readme_fp:
    long_description = readme_fp.read()


# This class is required since the askpass helper scripts need to be installed with execute permissions
class InstallLibrary(install):
    def run(self):
        install.run(self)
        for fn in self.get_outputs():
            if 'askpass' in fn and fn.endswith('.py'):
                os.chmod(fn, 0o777)

setup(
    name="pyautogit",
    version="0.0.2",
    author="Jakub Wlodek",
    author_email="jwlodek.dev@gmail.com",
    description="A command line interface for working with git written in python with the help of py_cui.",
    license="BSD 3-Clause",
    keywords="git command-line cli cui curses",
    url="https://github.com/jwlodek/pyautogit",
    long_description=long_description,
    long_description_content_type='text/markdown',
    cmdclass={'install':InstallLibrary},
    packages = find_packages(exclude=['tests', 'docs']),
    extras_require={
        'test': ['pytest'],
    },
    entry_points={
        'console_scripts': [
            'pyautogit = pyautogit:main',
        ],
    },
    install_requires=required_packages,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],

)