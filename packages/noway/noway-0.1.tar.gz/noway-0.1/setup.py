from setuptools import setup

with open("README.md", "r") as fh:

    long_description = fh.read()

setup(name='noway',
      version='0.1',
      description='Python interface to use the NoWay path planning application through redis.',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='http://github.com/rustyducks/noway-python',
      author='GuilhemBn@TheRustyDucks',
      author_email='buisanguilhem@gmail.com',
      license='LGPLv3',
      packages=['noway'],
      install_requires=[
            'redis'
      ],
      zip_safe=False)