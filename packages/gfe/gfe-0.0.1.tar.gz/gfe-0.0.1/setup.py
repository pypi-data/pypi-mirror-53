import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gfe",
    version="0.0.1",
    author="Pradeep Bashyal",
    author_email="pbashyal@nmdp.org",
    description="GFE",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nmdp-bioinformatics/GFE",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
