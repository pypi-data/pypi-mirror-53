import setuptools

with open("README.md", "r") as pkg:
    long_description = pkg.read()

setuptools.setup(
    name="comp-lead",
    version="0.0.1",
    author="Endormi",
    author_email="contactendormi@gmail.com",
    description="Display a handful of tech leaders",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/endormi/comp",
    packages=setuptools.find_packages(exclude=("tests",)),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)