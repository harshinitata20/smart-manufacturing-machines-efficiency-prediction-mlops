from setuptools import setup, find_packages
with open("requirements.txt") as f:
    requirements = f.read().splitlines()
setup(
    name="smart_manufacturing",
    version="0.1.0",
    author="Harshini",
    packages=find_packages(),
    install_requires=requirements,
)