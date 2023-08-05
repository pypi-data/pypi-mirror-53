import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dfpercentile-pkg-chanrl",
    version="0.0.1",
    author="Richard Chan",
    author_email="richard129chan@gmail.com",
    description="Package to separate a df by percentile on a column, bootstrap from the upper/lower bounds, create scatter plot and histogram, return p values on ttests and pearsons correlation coefficient",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chanrl/df-percentile",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
