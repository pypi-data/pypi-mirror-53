import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lod-domedi",
    version="0.0",
    author="David Eduard",
    author_email="edyalex.david@gmail.com",
    description="whatever",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EduardAlex/laughing-octo-doodle",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Public Domain",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)