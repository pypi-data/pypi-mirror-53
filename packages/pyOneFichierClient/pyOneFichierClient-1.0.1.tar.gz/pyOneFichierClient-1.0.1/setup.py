from distutils.core import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README-PyPI.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'pyOneFichierClient',         # How you named your package folder (MyLib)
  packages = ['pyOneFichierClient','pyOneFichierClient.setToken','pyOneFichierClient.OneFichierAPI'],   # Chose the same as "name"
  version = '1.0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'The coolest (and probably only for now) API on PyPI for 1ficher API access',   # Give a short description about your library
  long_description = long_description,
  long_description_content_type = 'text/rst',
  author = 'That Dude You Don\'t Want In Your Home',                   # Type in your name
  author_email = 'vidner123@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/spookyahell/pyOneFichierClient',   # Provide either the link to your github or to your website
  download_url = 'https://codeload.github.com/spookyahell/pyOneFichierClient/tar.gz/master',    # I explain this later on
  keywords = ['1FICHIER','API','CLIENT','FILEHOST'],   # Keywords that define your package best
  install_requires=['requests'],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)