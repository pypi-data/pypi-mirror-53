import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Eebuilder",
    version="1.0.0.1",
    author="Will F",
    author_email="forsbergw82@gmail.com",
    description="A Python package for creating HTML files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['web'],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    url='https://github.com/SuperMeteorite/Eebuilder',
)
