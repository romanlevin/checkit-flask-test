"""
Setup file for your Project
"""
from setuptools import setup, find_packages


install_requires = [
    'flask',
    'flask-restful',
    'python-dateutil',
]

tests_require = [
    'coverage',
    'nose-cov',
    'mock',
    'openstack.nose_plugin',
]

dependency_links = []

setup(
    name='app',
    version='1.0',
    description='',
    author='',
    packages=find_packages('src', exclude=['*.tests', ]),
    package_dir={'': 'src'},
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={
        'test': tests_require,
    },
    dependency_links=dependency_links,
    entry_points={}
)
