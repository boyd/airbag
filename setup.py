import os.path
from setuptools import setup, find_packages


ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__)))


setup(
    name='airbag',
    version='1.0.dev0',
    author='Patrick Boyd',
    author_email='pat.m.you-can-guess@gmail.com',
    description='Python crash report tool',
    long_description=open('README.md').read(),
    package_dir={'': 'src'},
    packages=find_packages('src', exclude=["*test"]),
    package_data={'airbag': ['*.*', 'src/airbag/*.*']},
    zip_safe=False,
    include_package_data=True,
)
