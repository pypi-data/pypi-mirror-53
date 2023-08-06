from distutils.core import setup
setup(
  name = 'superloop',         # How you named your package folder (MyLib)
  packages = ['superloop'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Inspired by a wide array of toolsets (unamed) used and developed by a leading social media tech company in the Bay Area for network automation, I have attempted to create my own version.',   # Give a short description about your library
  author = 'Wai Lit Loi',                   # Type in your name
  author_email = 'wailit@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/superloopnetwork',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/superloopnetwork/superloop/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['NETWORK AUTOMATION', 'SUPERLOOP', 'AUTOMATION'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'netmiko',
          'threading',
          're',
          'getpass',
          'time',
          'base64',
          'datetime',
          'os',
          'ciscoconfparse',
          'argparse',
          'subprocess',
          'yaml',
          'difflib',
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
