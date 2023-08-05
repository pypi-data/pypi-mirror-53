import glob
import os
from setuptools import find_packages, setup
import warnings


def here(filename):
    return os.path.join(os.path.dirname(__file__), filename)


def parse_requirements(filename):
    reqs = []
    with open(filename, "r") as fd:
        for line in fd:
            hash_idx = line.find("#")
            if hash_idx >= 0:
                line = line[:hash_idx]
            line = line.strip()
            if line and not line.startswith("-"):
                reqs.append(line)
    return reqs


def get_readme():
    """Get the README from the current directory. If there isn't one, return an empty string."""
    all_readmes = sorted(glob.glob("README*"))
    if len(all_readmes) > 1:
        warnings.warn(
            "There seems to be more than one README in this directory. Choosing the "
            "first in lexicographic order."
        )
    if all_readmes:
        return open(all_readmes[0], "r").read()
    warnings.warn("There doesn't seem to be a README in this directory.")
    return ""


setup(
    name="falcontool",
    version="0.1.1",
    url="https://github.com/timboring/falcontool",
    author="Tim Boring",
    author_email="tim@boring.green",
    scripts=["bin/falcon"],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=parse_requirements(here("requirements.txt")),
    description="Falcon commandline tool",
    long_description="".join(["\n", get_readme()]),
    long_description_content_type='text/markdown',
)
