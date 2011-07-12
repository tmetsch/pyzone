'''
Needed for setuptools...

Created on Jul 12, 2011

@author: tmetsch
'''
from distutils.core import setup

setup(name='pyzone',
      version='1.0',
      description='Ctypes wrappers to manage Solaris zones in Python.',
      license='???',
      author='Thijs Metsch',
      author_email='tmetsch@opensolaris.org',
      keywords='Solaris, Zones, Containers',
      url='http://www.github.org/tmetsch/pyzone',
      packages=['pyzone'],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Intended Audience :: Education',
          'Intended Audience :: Manufacturing',
          'Intended Audience :: Other Audience',
          'Intended Audience :: Science/Research',
          'Intended Audience :: System Administrators',
          'Operating System :: POSIX :: SunOS/Solaris',
          'Programming Language :: Python',
          'Topic :: Scientific/Engineering',
          'Topic :: Utilities'
                     ],
     )
