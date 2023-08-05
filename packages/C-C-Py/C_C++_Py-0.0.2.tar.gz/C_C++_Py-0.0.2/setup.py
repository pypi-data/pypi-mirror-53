import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="C_C++_Py",
    version="0.0.2",
    author="FeedFall8",
    author_email="FeedFall8@gmail.com",
    description="A big C++ Based python library instructions...to run type 'import CPP' twice use the 'CPP.doc()' function for info! ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://google.com",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
