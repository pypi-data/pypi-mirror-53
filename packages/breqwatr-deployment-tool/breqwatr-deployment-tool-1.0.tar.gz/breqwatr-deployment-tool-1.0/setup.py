"""Set up Breqwatr Deployment Tool package"""
from setuptools import setup, find_packages

with open('README.md', 'r') as readme_file:
    long_description = readme_file.read()

requirements = []
with open('requirements.txt', 'r') as reqs_file:
    requirements = reqs_file.read().splitlines()

setup(
    name='breqwatr-deployment-tool',
    packages=find_packages(),
    version='1.00',
    license='',
    description='Deploy and manage Breqwatr services',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Kyle Pericak',
    author_email='kyle@breqwatr.com',
    download_url='https://github.com/breqwatr/breqwatr-deployment-tool/archive/1.00.tar.gz',
    url='https://github.com/breqwatr/breqwatr-deployment-tool',
    keywords=['Breqwatr', 'Openstack', 'Kolla'],
    install_requires=requirements,
    entry_points='''
        [console_scripts]
        bwdt=bwdt.cli.main:main
    ''',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'Natural Language :: English'
    ]
)
