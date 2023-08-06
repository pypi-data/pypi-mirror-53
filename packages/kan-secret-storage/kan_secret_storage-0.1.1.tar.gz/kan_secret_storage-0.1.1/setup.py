from setuptools import setup, find_packages
from os.path import join, dirname
import kan_secret_storage

setup(
    name='kan_secret_storage',
    version=kan_secret_storage.__version__,
    description="Python Secret Storage package",
    packages=find_packages(exclude=["tests.*", "tests"]),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    install_requires=['pycryptodome'],
    author="Andrew KAN",
    author_email="kan@kansoftware.ru",
    license="GPL-3",
    url="https://github.com/kansoftware/secret_storage",
)
