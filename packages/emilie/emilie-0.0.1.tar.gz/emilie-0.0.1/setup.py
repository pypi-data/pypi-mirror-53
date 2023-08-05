import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="emilie",
    version="0.0.1",
    author="Emilie Schario",
    author_email="emilie.schario@gmail.com",
    description="Meet Emilie",
    long_description="Just Emilie Being Emilie Things",
    long_description_content_type="text/markdown",
    url="https://gitlab.com/emilie/emilie",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
