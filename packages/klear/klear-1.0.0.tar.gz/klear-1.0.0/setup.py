"""Packaging settings."""

from codecs import open
from os.path import abspath, dirname, join
from subprocess import call

from setuptools import Command, find_packages, setup

from klear import __version__

this_dir = abspath(dirname(__file__))
with open(join(this_dir, "README.md"), encoding="utf-8") as file:
    long_description = file.read()


class RunTests(Command):
    """Run all tests."""

    description = "run tests"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run all tests!"""
        print(__version__)
        errno = call(["pytest", "--cov=klear", "--cov-report=term-missing"])
        raise SystemExit(errno)


setup(
    name="klear",
    version=__version__,
    description="A minimal chat system.",
    long_description=long_description,
    url="https://gitlab.com/raiyanyahya/klear",
    author="Raiyan Yahya",
    author_email="raiyanyahyadeveloper@gmail.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "License :: Public Domain",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="cli",
    packages=find_packages(exclude=["docs", "tests*"]),
    install_requires=["click", "PyInquirer", "pyfiglet"],
    extras_require={"test": ["coverage", "pytest", "pytest-cov"]},
    entry_points={"console_scripts": ["klear=klear.cli:main"]},
    cmdclass={"test": RunTests},
)
