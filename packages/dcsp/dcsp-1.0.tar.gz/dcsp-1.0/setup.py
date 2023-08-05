from distutils.core import setup
setup(
  name = 'dcsp',         # How you named your package folder (MyLib)
  packages = ['dcsp'],   # Chose the same as "name"
  version = '1.0',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Drone Controlling and Streaming Protocol',   # Give a short description about your library
  author = 'Ömer Feyyaz Selçuk',                   # Type in your name
  author_email = 'omrfyyz@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/divisia/dcsp',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/divisia/dcsp/archive/1.0.tar.gz',    # I explain this later on
  keywords = ['drone', 'streaming', 'telemetry'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'zmq'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)