""" setup script of pycarsimlib """
import setuptools
import pycarsimlib

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pycarsimlib",
    version=pycarsimlib.__version__,
    install_requires=[
        "typing>=3.7.4.3",
        "rich>=12.6.0",
        "numpy>=1.19.5",
    ],
    entry_points={
        'console_scripts': [
        ],
    },
    author="MizuhoAOKI",
    author_email="mizuhoaoki1998@gmail.com",
    description="pycarsimlib: carsim wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MizuhoAOKI/pycarsimlib",
    download_url="https://github.com/MizuhoAOKI/pycarsimlib",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
