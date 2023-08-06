import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="geo58",
    version="1.0.0b1",
    author="Florian Klien",
    author_email="flowolf@klienux.org",
    description="Yet another short-link specification for geo-coordinates.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/flowolf/Geo58",
    # packages=setuptools.find_packages(),
    packages=setuptools.find_packages(exclude=['contrib', 'docs', 'tests']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: GIS",
    ],
    python_requires='>=3.6',
)
