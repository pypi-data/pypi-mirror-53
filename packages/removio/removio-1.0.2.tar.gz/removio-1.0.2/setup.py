import setuptools
from pathlib import Path

setuptools.setup(
    name='removio',
    version='1.0.2',
    scripts=['removio'] ,
    author="Vladimir Mikulic",
    author_email="vladimir.mikulic2@gmail.com",
    description="Remove any app from your Android device without root access.",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/VladimirMikulic/removio",
    license="MIT",
    packages=setuptools.find_packages(),
    classifiers=[
        "Environment :: Console",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=[
        "android",
        "app",
        "remove"
    ]
 )