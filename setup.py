from setuptools import setup
from sys import platform

required_packages = ['py_cui']
if platform == "win32":
    required_packages.append('wexpect')
else:
    required_packages.append('pexpect')


setup(
    name="pyautogit",
    version="0.0.1",
    author="Jakub Wlodek",
    author_email="jwlodek.dev@gmail.com",
    description="A command line interface for working with git written in python with the help of py_cui.",
    license="BSD 3-Clause",
    keywords="git command-line cli cui curses",
    url="https://github.com/jwlodek/pyautogit",
    long_description=read("README.md")
    long_description_content_type='text/markdown',
    extras_require={
        'test': ['pytest'],
    },
    entry_pointe={
        'console_scripts' :[
            'pyautogit=pyautogit:main'
        ],
    },
    install_requires=required_packages,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

)