from setuptools import setup, find_packages

setup(
    name='dyntree',
    version='0.0.1',
    url='https://bitbucket.org/submax82/dyntree',
    author='Massimo Cavalleri',
    author_email='submax@tiscali.it',
    description='Provides possibility to create and manage tree built by id and parent for every node',
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
