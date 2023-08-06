import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='infusionsoft-python',
      version='0.1.3',
      description='API wrapper for Infusionsoft written in Python',
      long_description=read('README.md'),
      long_description_content_type="text/markdown",
      url='https://github.com/GearPlug/infusionsoft-python',
      author='Yordy Gelvez',
      author_email='yordy.gelvez@gmail.com',
      license='MIT',
      packages=['infusionsoft'],
      install_requires=[
          'requests',
      ],
      zip_safe=False)
