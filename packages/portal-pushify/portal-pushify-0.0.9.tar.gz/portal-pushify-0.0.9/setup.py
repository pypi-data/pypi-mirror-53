import os
from setuptools import setup

README_PATH = open(
    os.path.join(os.path.dirname(__file__), 'README.md')
)
with README_PATH as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(
    os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir))
)

VERSION = '0.0.9'

setup(
    name='portal-pushify',
    version=VERSION,
    packages=[
        'portal-pushify',
    ],
    include_package_data=True,
    license='MIT License',
    description='Simple http rest api to cmd line interface.',
    long_description=README,
    url='https://github.com/colask8/portal-pushify.git',
    download_url='https://github.com/colask8/portal-pushify/tarball/%s' % VERSION,
    author='Stojan Veljkovic',
    author_email='cola14@gmail.com',
    install_requires=[
        'flask==1.0.2',
        'Flask-SocketIO==4.1.0',
        'gunicorn==19.9.0',
        'pyyaml==5.1b3'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
