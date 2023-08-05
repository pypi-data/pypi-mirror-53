from setuptools import setup, find_packages

setup(name="scapywrapper",
      version="1.0",
      description="Basic Python wrapper to extend the built-in capabilities of the scapy package",
      url="https://github.com/guyavrah1986/scapywrapper.git",
      author="Guy Avraham",
      author_email="guyavrah1986@gmail.com",
      license="GPL-2.0",
      packages=find_packages(exclude=["tests"]),
      include_package_data=True,
      install_requires=["scapy"])
