from setuptools import find_packages, setup

setup(
    author="TAOS DevopsNow",
    name="taosdevopsutils",
    description="Utility Functions for the Taos Devops team",
    # license=open("LICENSE").read(),
    long_description=open("README.rst").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    version="0.0.1",
    url="https://github.com/taosdevops/taos-devops-utils",
    install_requires=[
        "aiohttp==4.0.0a0",
        "async-timeout==3.0.1",
        "attrs==19.1.0",
        "certifi==2019.9.11",
        "chardet==3.0.4",
        "idna==2.8",
        "multidict==4.5.2",
        "requests==2.22.0",
        "slackclient==2.2.0",
        "urllib3==1.25.6",
        "yarl==1.3.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
)
