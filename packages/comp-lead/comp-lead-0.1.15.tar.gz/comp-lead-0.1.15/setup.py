import setuptools

with open("README.md", "r") as pkg:
    long_description = pkg.read()

setuptools.setup(
    name="comp-lead",
    version="0.1.15",
    author="Endormi",
    author_email="contactendormi@gmail.com",
    description="Display a handful of tech leaders and companies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/endormi/comp-lead",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
)