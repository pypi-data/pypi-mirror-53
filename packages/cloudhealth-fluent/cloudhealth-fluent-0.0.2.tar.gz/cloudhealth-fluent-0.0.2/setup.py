import os
import setuptools
from distutils.core import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
  name='cloudhealth-fluent',
  packages=setuptools.find_packages(),
  version='0.0.2',
  description='CloudHealth fluent interface',
  long_description=read('README.md'),
  long_description_content_type='text/markdown',
  author='troylar',
  author_email='troylar@pm.me',
  url='https://github.com/awslabs/cloudhealth-fluent',
  keywords=['cloudhealth'],
  license="Apache-2.0",
  classifiers=[
      "Development Status :: 5 - Production/Stable",
      "Topic :: Utilities",
      "License :: OSI Approved :: Apache Software License",
  ]
)
