from horn import __version__
from setuptools import setup


setup_data = {
    'name': 'horn-py',
    'version': __version__,
    'author': 'bigfang',
    'author_email': '',
    'description': 'A Flask scaffolding tool',
    'license': 'MIT',
    'keywords': 'flask scaffolding',
    'classifiers': [
        'Topic :: Utilities',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    'install_requires': [
        'docopt>=0.6',
        'copier>=2.3.3',
    ],
    'entry_points': {
        'console_scripts': ['horn = horn:main', ],
    }
}


setup(**setup_data)
