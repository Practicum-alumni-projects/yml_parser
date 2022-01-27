from cx_Freeze import setup, Executable

executables = [Executable('parser.py')]

setup(name='parser',
      version='1.0',
      description='google sheet to yml',
      executables=executables)
