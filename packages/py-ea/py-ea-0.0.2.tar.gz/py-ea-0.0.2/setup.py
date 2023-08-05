import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="py-ea",
    version="0.0.2",
    author="mariusaarsnes",
    author_email="marius.aarsnes@gmail.com",
    description="Evolutionary algorithms written in python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mariusaarsnes/py-ea",
    packages=setuptools.find_packages(),
    classifiers=["Programming Language :: Python :: 3",
                 "License :: OSI Approved :: MIT License",
                 "Operating System :: OS Independent"],
    python_requires='>=3.6.8'
)
