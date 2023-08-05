# --------------------------------------------------------------------------
# Company:      DecisionVis LLC
# Description:  DiscoveryDV/setup.py
# Author:       Joshua Kollat
# Created:      8/9/2019
# Copyright:    (c) 2012-2019
# License:      MIT License
# --------------------------------------------------------------------------

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DiscoveryDV",
    version="0.3",
    author="DecisionVis LLC",
    author_email="team@decisionvis.com",
    description="Python package for interfacing with DiscoveryDV using its API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.decisionvis.com/ddv/",
    packages=setuptools.find_packages(),
    install_requires=["pyzmq","msgpack-python"],
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)