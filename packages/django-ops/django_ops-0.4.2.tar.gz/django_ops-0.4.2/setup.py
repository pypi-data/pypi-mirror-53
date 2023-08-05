import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django_ops',
    version='0.4.2',
    packages=["django_ops"],
    include_package_data=True,
    license='BSD License',  # example license
    description='A simple Django app for common django_ops utilities',
    long_description=README,
    long_description_content_type='text/x-rst',
    url='https://www.example.com/',
    author='Alan',
    author_email='alan@hkasianark.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    python_requires=">=3.5",
    install_requires=[
        "Django",
        "djangorestframework",
        "psycopg2-binary",
        "psutil",
    ],
)
