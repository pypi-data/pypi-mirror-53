from setuptools import setup, find_packages

setup(name='subscription-parser',
      version='0.1',
      description='A python package to parse SS/SSR subscription link',
      url='http://https://github.com/0KABE/subscription-parser',
      author='0KABE',
      author_email='RIN.OKAB3@GMAIL.COM',
      license='MIT',
      packages=find_packages(),
      install_requires=["aiohttp"]
)
