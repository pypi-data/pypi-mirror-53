from setuptools import setup
from install_requires import install_requires

setup(
   name='pipenvExample',
   version='0.1.1',
   description='Example pipenv project',
   author='Alan Bacon',
   author_email='alan@bacontowers.co.uk',
   packages=['pipenvExample'],
   install_requires=install_requires
)