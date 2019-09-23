import io
import re

from setuptools import find_packages, setup

with io.open("README.rst", "rt", encoding="utf8") as f:
    readme = f.read()

with io.open("requirements.txt", "rt", encoding="utf8") as f:
    requirements = f.read()

with io.open("obs/__init__.py", "rt", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

setup(
    name="neo-obs",
    version=version,
    description="A OBS command line tools",
    long_description=readme,
    url="https://github.com/BiznetGIO/neo-obs",
    author="BiznetGio",
    author_email="support@biznetgio.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "License :: MIT",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="cli",
    include_package_data=True,
    packages=find_packages(exclude=["docs", "tests*"]),
    install_requires=requirements,
    entry_points={"console_scripts": ["obs=obs.main:cli"]},
)
