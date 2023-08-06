from setuptools import setup
long_description = ""


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='lcdk',
      version='0.2',
      description='Leslie Chow Debug Kit',
      url='https://github.com/senorChow/lcdk.git',
      author='John M. Cook',
      long_description = long_description,
      long_description_content_type="text/markdown",
      author_email='jmcook1982@protonmail.com',
      license='MIT',
      packages=['lcdk'],
      zip_safe=False)
