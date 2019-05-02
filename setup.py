from horn import __version__
from setuptools import find_packages, setup


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
    'zip_safe': True,
    'include_package_data': True,
    'packages': find_packages(),
    'install_requires': [
        'docopt>=0.6',
        'toml>=0.10.0',
        'copier>=2.3.3',
        'pampy==0.2.1',
    ],
    'entry_points': {
        'console_scripts': ['horn = horn:main'],
    }
}


setup(**setup_data)
