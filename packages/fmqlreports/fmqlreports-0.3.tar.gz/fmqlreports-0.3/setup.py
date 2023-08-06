from setuptools import setup

setup(name='fmqlreports',
      description = 'FMQL Reports',
      long_description = """A Python framework and set of executables for generating specific reports on VistA data cached using FMQL.""",
      version='0.3',
      install_requires = [
          'fmqlutils>=2.92'
          # 'numpy>=1.16.3'
      ],
      classifiers = ["Development Status :: 4 - Beta", "Programming Language :: Python :: 2.7"],
      url='http://github.com/Caregraf/FMQL/fmqlreports',
      license='Apache License, Version 2.0',
      keywords='VistA,FileMan,CHCS,FMQL,Caregraf',
      # install_requires=["pytz"], - problem OSX 
      package_dir = {'fmqlreports': ''},
      packages = ['fmqlreports', 'fmqlreports.basics', 'fmqlreports.patient', 'fmqlreports.user', 'fmqlreports.schema', 'fmqlreports.imaging'],
      entry_points = {
      }
)
