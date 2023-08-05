from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='coinpy',
      version='1.2',
      description='Gaussian distributions',
      long_description=long_description,
      long_description_content_type="text/markdown",
      packages=['coinpy'],
      zip_safe=False,
      url="https://github.com/feeblefruits/coinpy",
      author="Jacques Coetzee",
      author_email="j.coetzee0@gmail.com",
      license="MIT")