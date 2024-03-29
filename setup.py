# -*- coding: utf-8 -*-

from setuptools import find_packages, setup


def requirements(filename):
    """Reads requirements from a file."""
    with open(filename) as f:
        return [x.strip() for x in f.readlines() if x.strip()]


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(name='boj2md',
      version='0.0.2',
      description='Parse Baekjoon Online Judge Problem to Markdown',
      long_description=readme(),
      long_description_content_type='text/markdown',
      author='Chanwoong Kim',
      author_email='me@chanwoong.kim',
      url='https://github.com/kexplo/boj2md',
      packages=find_packages(),
      entry_points={
          'console_scripts': ['boj2md = boj2md:main']
      },
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.7',
          'Topic :: Utilities',
      ],
      install_requires=requirements('requirements.txt'),
      # tests_require=requirements('tests/requirements.txt'),
      )
