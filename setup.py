from setuptools import setup, find_packages
from cliparse import __version__

LONG_DESCRIPTION = open("README.md", "r", encoding="utf-8").read()

setup(
    name="cliparse",
    version=__version__,
    author="Duk Kyu Lim",
    author_email="hong18s@gmail.com",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    description='CLI Framework with Argparse',
    url="https://github.com/ravenkyu/cliparse",
    license="MIT",
    keywords="cli",
    install_requires=[
        'tabulate',
    ],
    packages=find_packages(
        exclude=['sample_cli', 'sample_cli.*', 'tests', 'tests.*']),
    package_data={},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
    zip_safe=False,
)
