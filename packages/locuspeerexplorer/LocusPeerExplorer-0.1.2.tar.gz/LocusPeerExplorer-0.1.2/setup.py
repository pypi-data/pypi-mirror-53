from distutils.core import setup
setup(
  name='LocusPeerExplorer',         # How you named your package folder (MyLib)
  packages=['LocusPeerExplorer'],   # Chose the same as "name"
  version='0.1.2',      # Start with a small number and increase it with every change you make
  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  license='MIT',
  # Give a short description about your library
  description='A package that lets you find similar community peers based off of functional or outcomee data',
  author='Locus Analytics',                   # Type in your name
  author_email='alee@locus.co',      # Type in your E-Mail
  # Provide either the link to your github or to your website
  url='https://github.com/user/reponame',
  download_url='https://github.com/LocusAnalytics/peer-explorer/archive/v0.1.post2.tar.gz',
  # Keywords that define your package best
  keywords=['Economics', 'Peer Finder'],
  install_requires=[            # I get to this in a second
          'numpy',
          'pandas',
          'scipy',
          'fastdtw',
      ],
  classifiers=[
    # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Development Status :: 3 - Alpha',
    # Define that your audience are developers
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    # Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
