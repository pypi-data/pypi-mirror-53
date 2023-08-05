"""setup.py"""
import setuptools

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name='vbiz_parser',
    version='0.1.31',
    author='Kris Luu',
    author_email='luuthaidangkhoa@gmail.com',
    description='The vBiz parser',
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url='https://github.com/ltdangkhoa/vbiz_parser',
    packages=setuptools.find_packages(),
    install_requires=[
        'pdfminer.six',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': ['vbiz_parser=vbiz_parser.command_line:main'],
    },
    include_package_data=True,
    zip_safe=False)
