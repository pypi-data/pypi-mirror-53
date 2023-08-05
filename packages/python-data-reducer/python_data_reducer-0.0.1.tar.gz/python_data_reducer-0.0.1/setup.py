import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python_data_reducer",
    version="0.0.1",
    author="Tri Nguyen",
    author_email="tringuyen5835@gmail.com",
    description="This package help you to easily reduce the data input",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shinrel22/data_reducer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)
