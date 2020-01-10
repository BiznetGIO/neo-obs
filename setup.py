import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open("obs/cli/__init__.py", "r", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

with open("README.rst", "rb") as f:
    readme = f.read().decode("utf-8")

with open("requirements.txt", "rb") as f:
    requirements = f.read().decode("utf-8")

setup(
    name="neo-obs",
    version=version,
    description="A OBS command line tools",
    long_description=readme,
    long_description_content_type="text/x-rst",
    url="https://github.com/BiznetGIO/neo-obs",
    author="BiznetGio",
    author_email="support@biznetgio.com",
    license="MIT license",
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="cli",
    include_package_data=True,
    packages=["obs"],
    install_requires=requirements,
    entry_points={"console_scripts": ["obs=obs.main:cli"]},
)
