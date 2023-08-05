"""Package definition for bb2cc."""

from distutils.core import setup

setup(
    name='bb2cc',
    version='0.6.0',
    url='https://bitbucket.org/dtao/bb2cc',
    license='MIT',
    author='Dan Tao',
    author_email='dtao@atlassian.com',
    description='Bitbucket to Confluence Cloud',
    py_modules=['cc', 'md2cc', 'util'],
    scripts=['bin/bb2cc'],
    install_requires=[
        'requests==2.22.0',
        'mistune==0.8.4',
        'pyyaml==5.1.2'
    ],
    tests_require=[
        'pytest>=5.1.3'
    ]
)
