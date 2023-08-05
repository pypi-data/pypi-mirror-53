"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

import os

# To use a consistent encoding
from codecs import open

# Always prefer setuptools over distutils
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

# recursively add data files
rootDir = "nowyou_vstitcher_script_python/vstitcher_plugins"
data_files = [os.path.relpath(os.path.join(dirpath, file), rootDir) for (dirpath, dirnames, filenames) in os.walk(rootDir) for file in filenames]

setup(
    name="nowyou_vstitcher_script_python",
    version="0.1.49",
    description="Nowyou VStitcher script python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # The project's main homepage.
    url="https://bitbucket.org/inventilabs/nowyou-vstitcher-script-python/",
    # Author details
    author="Alex Mensak",
    author_email="alexander.mensak@ilabs.cz",
    # Choose your license
    license="proprietary",
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3",
    ],
    keywords="nowyou python",
    package_data={
        'nowyou_vstitcher_script_python.vstitcher_plugins': data_files,
        'nowyou_vstitcher_script_python.utils': ['*'],
    },
    packages=["nowyou_vstitcher_script_python", "nowyou_vstitcher_script_python.model",
              "nowyou_vstitcher_script_python.tasks", "nowyou_vstitcher_script_python.utils",
              "nowyou_vstitcher_script_python.vstitcher_plugins"],
    install_requires=['pyautogui'],
    python_requires=">=3.6",
    # extras_require={"dev": ["pytest"]},
)
