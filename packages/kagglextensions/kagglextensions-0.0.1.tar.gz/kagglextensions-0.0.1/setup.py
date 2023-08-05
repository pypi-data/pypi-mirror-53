import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kagglextensions",
    version="0.0.1",
    author="Giovanni Borghi",
    author_email="gio.borghi@gmail.com",
    description="A package for extending kaggle",
    long_description="NO DESCRIPTION",
    long_description_content_type="text/markdown",
    url="https://github.com/gborghi/kagglextensions.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
    requires=['math']
)
