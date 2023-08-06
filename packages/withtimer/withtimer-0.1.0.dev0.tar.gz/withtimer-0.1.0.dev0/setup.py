from __future__ import absolute_import
from setuptools import setup
about = {}
with open("withtimer/__about__.py") as fp:
    exec(fp.read(), about)

with open("README.md", "r") as fp:
    long_description = fp.read()

setup(name=about["__title__"],
      version=about["__version__"],
      description=about["__summary__"],
      long_description=long_description,
      license="MIT",
      author="Zachary Cutlip",
      long_description_content_type="text/markdown",
      url="https://github.com/zcutlip/withtimer",
      packages=['withtimer'],
      python_requires='>=2.7',
      install_requires=[],
      package_data={'withtimer': ['config/*']},
      )
