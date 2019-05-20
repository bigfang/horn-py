from setuptools import find_packages, setup

from horn import __version__


with open('README.md', 'r') as f:
    readme = f.read()


setup_data = {
    'name': 'horn-py',
    'version': __version__,
    'author': 'bigfang',
    'author_email': 'bitair@gmail.com',
    'description': 'A Flask scaffolding tool',
    'long_description': readme,
    'long_description_content_type': 'text/markdown',
    'license': 'MIT',
    'keywords': 'flask scaffolding',
    'classifiers': [
        'Topic :: Utilities',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
    ],
    'zip_safe': True,
    'include_package_data': True,
    'packages': find_packages(),
    'install_requires': [
        'docopt>=0.6',
        'toml>=0.10.0',
        'inflection>=0.3.1',
        'pampy>=0.2.1',
        'copier==2.3.3',
    ],
    'entry_points': {
        'console_scripts': ['horn = horn:main'],
    }
}

setup(**setup_data)
