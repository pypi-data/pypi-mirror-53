from distutils.core import setup

setup(
  name = 'memory3',
  packages = ['memory'],
  version = '19.09.25',
  license='gpl-3.0',
  description = 'Lightweight json-based config manager.',
  author = 'Kaiser',
  author_email = 'technomancer@gmx.com',
  url = 'https://github.com/codedthoughts/memory3',
  download_url = 'https://github.com/codedthoughts/memory3/archive/19.09.25.tar.gz',
  keywords = ['json', 'config', 'manager'],
  install_requires=[
          'humanfriendly',
      ],
  classifiers=[
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 4 - Beta',

    # Indicate who your project is intended for
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    
    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)
