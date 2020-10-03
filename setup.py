from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
   name='venues',
   version='1.0',
   description='Check which venues are suitable for all users.',
   license="MIT",
   author='Paulo Henrique',
   author_email='paulohsilvapinto@gmail.com',
   url="https://github.com/paulohsilvapinto/timeout-test",
   packages=['venues'],
   install_requires=requirements
)
