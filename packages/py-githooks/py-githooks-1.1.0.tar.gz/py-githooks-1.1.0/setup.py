import os
import sys
import pathlib
from setuptools import setup
from setuptools.command.install import install

import python_githooks

HERE = pathlib.Path(__file__).parent

VERSION = python_githooks.__version__

README = (HERE / "README.md").read_text()


class VerifyVersionCommand(install):
    """Command to verify that the git tag matches the library version"""

    description = "verify that the git tag matches the library version"

    def run(self):
        tag = os.getenv("CIRCLE_TAG").replace("v", "")

        if tag != VERSION:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, VERSION
            )
            sys.exit(info)


setup(
    name="py-githooks",
    version=VERSION,
    description="Create git hooks with ease using a simple configuration file in a git project",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/iamogbz/python-githooks",
    author="Emmanuel Ogbizi-Ugbe",
    author_email="iamogbz+pygithooks@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
    ],
    packages=["python_githooks"],
    include_package_data=True,
    install_requires=["configparser"],
    entry_points={"console_scripts": ["githooks=python_githooks.__main__:main"]},
    cmdclass={"verify": VerifyVersionCommand},
)
