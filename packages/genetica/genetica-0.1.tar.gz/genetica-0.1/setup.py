# from distutils.core import setup
from setuptools import setup
setup(
  name = 'genetica',
  packages = ['genetica'],
  version = '0.1',
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'This library allows you to take any class with certain business logic, modify it a \
   little and then give it back to Genetica to optimize.',   # Give a short description about your library
  author = 'Vladimir Semenov',                   # Type in your name
  author_email = 'subatiq@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/VASemenov/genetica',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/VASemenov/genetica/archive/0.1.tar.gz',    # I explain this later on
  keywords = ['genetic', 'optimization', 'minimalistic'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'matplotlib',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)