from setuptools import setup

setup(name='nfl_insights',
      version='0.1.43',
      description='Contendo.ai nfl insights package',
      url='https://github.com/sportsight-pro/sportsight-core/tree/master/nfl_insights',
      author='Yahali Sherman, contendo.ai',
      author_email='yahali@contendo.ai',
      license='MIT',
      packages=['nfl_insights', 'nfl_insights/queries'],
      install_requires=[
          'contendo_utils',
          'gspread_pandas',
      ],
      zip_safe=False)
