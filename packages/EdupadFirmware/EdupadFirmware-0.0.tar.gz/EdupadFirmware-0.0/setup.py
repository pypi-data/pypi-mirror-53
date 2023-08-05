# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 12:26:05 2019

@author: mesci
"""

from distutils.core import setup

setup(
  name = 'EdupadFirmware',         # How you named your package folder (MyLib)
  packages = ['EdupadFirmware'],   # Chose the same as "name"
  version = '0.0',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Library for Edupad',   # Give a short description about your library
  author = 'Tinkrz',                   # Type in your name
  author_email = 'renuka.angole@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/user/reponame',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/RenukaAngole1/EdupadFirmware/archive/0.0.tar.gz',    # I explain this later on
  keywords = ['Edupad', 'Hardware', 'Activities'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pyserial',
          'requests',
          'pyttsx3',
          'PyAudio-0.2.11-cp37-cp37m-win_amd64.whl',
          'SpeechRecognition',
          'python-vlc',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    
    'Programming Language :: Python :: 3.7'
  ],
)