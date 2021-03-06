from distutils.core import setup
setup(
  name = 'NHLArenaAdjuster',         # How you named your package folder (MyLib)
  packages = ['NHLArenaAdjuster'],   # Chose the same as "name"
  version = '0.1.4',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'This is a package made to adjust the event-coordinate data available from the NHL API using the methodology proposed'
                ' by Shuckers & Curro in "Total Hockey Rating (THoR): A comprehensive statistical rating of National Hockey'
                ' League forwards and defensemen based upon all on-ice events"',   # Give a short description about your library
  author = 'Nathan de Lara',                   # Type in your name
  author_email = 'nathandelara1@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/delara38/NHLArenaAdjuster',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/delara38/NHLArenaAdjuster/releases/tag/0.1.2#:~:text=Source%20code,(zip)',    # I explain this later on
  keywords = ['HOCKEY','NHL'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'numpy',
          'pandas',
          'statsmodels',
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
