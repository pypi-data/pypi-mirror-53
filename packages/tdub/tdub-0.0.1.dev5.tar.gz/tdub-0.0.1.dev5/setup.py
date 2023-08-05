from setuptools import setup
from setuptools import find_packages
import os


with open("requirements.txt") as f:
    requirements = f.read().splitlines()


this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), "rb") as f:
    long_description = f.read().decode("utf-8")


def get_version():
    with open(os.path.join("tdub", "__init__.py"), "r") as f:
        for line in f.readlines():
            if "__version__ = " in line:
                return line.strip().split(" = ")[-1][1:-1]


setup(
    name="tdub",
    version = get_version(),
    scripts=[],
    packages=find_packages(exclude=["tests"]),
    entry_points={"console_scripts": ["tdub = tdub._app:cli"]},
    description="tdub is tee double-you",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Doug Davis",
    author_email="ddavis@ddavis.io",
    maintainer="Doug Davis",
    maintainer_email="ddavis@ddavis.io",
    license="BSD 3-clause",
    url="https://github.com/douglasdavis/tdub",
    test_suite="tests",
    python_requires=">=3.7",
    install_requires=requirements,
    tests_require=["pytest>=4.0"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",

    ],
)
