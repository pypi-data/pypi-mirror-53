"""
Created on Sun Sep 29
For Mango Solutions Python test
For any questions please contact Claire Blejean: claire.blejean@gmail.com

"""

from distutils.core import setup
setup(
  name = 'mango_programming_test',
  packages = ['mango_programming_test'], 
  version = '0.11', 
  license = 'MIT',
  description = 'Package developed for Mango Solutions programming test.',
  author = 'Claire Blejean',
  author_email = 'claire.blejean@gmail.com',
  url = 'https://github.com/ToMountainTops',
  download_url = 'https://github.com/ToMountainTops/mango_programming_test/archive/v_0.1.tar.gz',
  install_requires=[
          'numpy',
          'matplotlib',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)