import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="segcheck",
    version="0.0.1",
    author="thomasschus",
    author_email="thomas.schus@gmail.com",
    description="segcheck helps to find gaps and overlaps in linear segments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thomasschus/segcheck",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
