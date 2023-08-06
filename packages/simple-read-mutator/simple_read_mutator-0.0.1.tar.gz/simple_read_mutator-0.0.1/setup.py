from setuptools import setup

setup(name='simple_read_mutator',
      version='0.0.1',
      description='Simple Read Mutator',
      url='http://github.com/ivargr/simple_read_mutator',
      author='Ivar Grytten',
      author_email='',
      license='MIT',
      packages=['simple_read_mutator'],
      zip_safe=False,
      install_requires=['numpy'],
      classifiers=[
            'Programming Language :: Python :: 3'
      ])

"""
To update package:
#Update version number manually in this file

sudo python3 setup.py sdist
sudo python3 setup.py bdist_wheel
twine upload dist/simple_read_mutatot-X.tar.gz
"""
