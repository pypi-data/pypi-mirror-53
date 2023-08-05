import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="logify",
    version="0.0.1",
    author="Kelvin Tsoi",
    author_email="kelvin@hellospork.com",
    description="Python package for script logging and DataDog integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tsoisauce/klog",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "termcolor",
    ],
    python_requires='>=3.7',
)
