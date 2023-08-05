import setuptools

import sugarrush

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sugarrush",
    version=sugarrush.__version__,
    author="Jonatan Westholm",
    author_email="jonatanwestholm@gmail.com",
    description="Quality-of-life and extra features for python-sat",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jonatanwestholm/sugarrush",
    #packages=setuptools.find_packages(),
    packages=['sugarrush', 'sugarrush.examples'],
    package_dir={'sugarrush.examples': 'sugarrush/examples'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
