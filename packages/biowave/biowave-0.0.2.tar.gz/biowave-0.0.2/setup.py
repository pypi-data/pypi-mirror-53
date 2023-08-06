import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="biowave",
    version="0.0.2",
    author="Faruq Sandi",
    author_email="alice@example.com",
    description="Biosignal wrapper pipeline",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/faruqsandi/biowave",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)