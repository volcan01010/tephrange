import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="tephrange",
    version="0.1.0",
    description="Python functions to calculate tephra terminal velocity and transport range",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/volcan01010/tephrange",
    author="Dr John A Stevenson",
    author_email="johnalexanderstevenson@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Atmospheric Science"
    ],
    packages=["tephrange"],
    include_package_data=True,
    install_requires=["numpy"],
)
