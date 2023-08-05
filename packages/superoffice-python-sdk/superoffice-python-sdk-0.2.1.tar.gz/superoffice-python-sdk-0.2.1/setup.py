from setuptools import setup, find_packages

long_description = '''
SuperOffice Rest API Python SDK
'''

setup(
    name='superoffice-python-sdk',
    version='0.2.1',
    author='Ignotas Petrulis',
    author_email='ignotas.petrulis@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests'
    ],
    description='SuperOffice Python SDK',
    long_description=long_description
)
