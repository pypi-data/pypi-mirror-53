from distutils.core import setup

setup(
  name = 'g5-lambda-psycopg2',
  packages = ['psycopg2'],
  version = '0.1.7',
  license='MIT',
  description = 'Fork of awslambda-psycopg2',
  long_description="""
psycopg2 Python Library for AWS Lambda
======================================

This is a custom compiled psycopg2 C library for Python. Due to AWS Lambda
missing the required PostgreSQL libraries in the AMI image, we needed to
compile psycopg2 with the PostgreSQL `libpq.so` library statically linked
libpq library instead of the default dynamic link.

### How to use

This project only exists for python 3.7. The subsequent pypi package will only support python 3.7 as well.
It only includes the `with_ssl_support` version. Since that will generally be required for AWS lambda usage.

### Building from source
Go to the original package if you wish to modify this from source
""",
  long_description_content_type='text/markdown',
  author = 'G5Dev',
  author_email = 'g5dev@g5searchmarketing.com',
  url = 'https://github.com/G5/awslambda-psycopg2',
  download_url = 'https://github.com/G5/awslambda-psycopg2/archive/master.zip',
  package_data={'psycopg2': ['*.so', 'psycopg2/_psycopg.so']},
  include_package_data=True,
  keywords = ['aws', 'lambda', 'psycopg2'],
  install_requires=[],
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.7',
  ],
)
