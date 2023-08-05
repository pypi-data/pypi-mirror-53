from setuptools import find_packages
from setuptools import setup

with open('README.md', 'r') as readme:
    long_description = readme.read()

setup(
    name='flask_easyjwt',
    version='0.1.0',
    packages=find_packages(exclude=['docs', 'tests*']),

    python_requires='>=3.6',
    install_requires=[
        'easyjwt==0.1.*',
        'Flask>=1.0',
    ],

    author='Bastian Meyer',
    author_email='bastian@bastianmeyer.eu',
    url='https://github.com/BMeu/Flask-EasyJWT',
    project_urls={
        'Documentation': 'https://flask-easyjwt.readthedocs.io/en/latest/',
        'Source': 'https://github.com/BMeu/Flask-EasyJWT',
        'Tracker': 'https://github.com/BMeu/Flask-EasyJWT/issues',
    },

    description='Super simple JSON Web Tokens for Flask',
    long_description=long_description,
    long_description_content_type='text/markdown',

    keywords='jwt token tokens JSON Flask',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    zip_safe=False,
    include_package_data=True,
    platforms='any',
)
