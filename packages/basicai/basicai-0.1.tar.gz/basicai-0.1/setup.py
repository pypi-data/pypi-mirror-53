from setuptools import setup

setup(name='basicai',
      version='0.1',
      description='...',
      url='http://github.com/dejanbatanjac/basicai',
      author='Dejan Batanjac',
      author_email='dejan.batanjac@gmail.com',
      license='Apache 2.0',
      packages=['basicai'],
      install_requires = ['torch>=1.0', 'numpy'],
      zip_safe=False)