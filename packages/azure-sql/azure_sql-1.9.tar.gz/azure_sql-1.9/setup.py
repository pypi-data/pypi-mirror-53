from setuptools import setup
import os
setup(
  name = 'azure_sql',         # How you named your package folder (MyLib)
  packages = ['azure_sql'],   # Chose the same as "name"
  package_data={
    'azure_sql': ['py','*.hy',"*.json","*.md"]
  },
  version = '1.09',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Azure Database done easy',   # Give a short description about your library
  #long_description_markdown_filename='azure_sql/README.md',
  author = 'Ognjen/ShinSheel',                   # Type in your name
  author_email = 'vlad.g@simporter.com',      # Type in your E-Mail
  url = 'https://github.com/user/reponame',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['Azure', 'SQL', 'third party',"MySQL","Transact SQL"],   # Keywords that define your package best
  setup_requires=['setuptools-markdown'],
  install_requires=[            # I get to this in a second
          'requests','pyodbc','pandas','sqlalchemy',
          
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
  ],
)
