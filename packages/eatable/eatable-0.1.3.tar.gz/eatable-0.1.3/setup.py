import setuptools

with open("README.md", 'r') as f:
    long_description = f.read()


setuptools.setup(
    name="eatable",
    version="0.1.3",
    author="sirius demon",
    author_email="mory2016@126.com",
    description="Eatable Code",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/eatable-code/eatable",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
