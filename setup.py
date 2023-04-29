from setuptools import setup, find_packages
from pip._internal.req import parse_requirements
from pip._internal.network.session import PipSession

with open("README.md", "r") as fh:
    long_description = fh.read()

install_reqs = parse_requirements('requirements.txt', session=PipSession())
reqs = [str(ir.requirement) for ir in install_reqs]

setup(
    name="fakegeo-polychessbot",
    version="0.0.1",
    author="michael2to3",
    author_email="michael2ga3@gmail.com",
    description="bypass live location detect",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/michael2to3/fakegeo-polychessbot",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL-3.0",
        "Operating System :: OS Independent",
    ],
    install_requires=reqs
)
