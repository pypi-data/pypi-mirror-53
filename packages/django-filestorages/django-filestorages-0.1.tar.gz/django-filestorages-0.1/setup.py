import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='django-filestorages',
    version='0.1',
    author='Radek Czajka',
    author_email='rczajka@rczajka.pl',
    description='Configurable file storages for Django',
    long_description = long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/rczajka/django-filestorages',
    packages=setuptools.find_packages(where='src'),
    package_dir={"": "src"},
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'Django',
    ],
)
