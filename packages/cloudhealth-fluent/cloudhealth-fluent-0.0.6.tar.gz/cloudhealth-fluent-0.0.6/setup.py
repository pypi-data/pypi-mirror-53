import os
import setuptools


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
  name='cloudhealth-fluent',
  install_requires=required,
  version='0.0.6',
  description='CloudHealth fluent interface',
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
