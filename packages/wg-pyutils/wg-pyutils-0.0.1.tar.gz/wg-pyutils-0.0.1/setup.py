import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wg-pyutils",
    version="0.0.1",
    author="wg",
    author_email="wugifer@pku.org.cn",
    description="This is a Python package containing lots of small and useful functions for reuse",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wugifer/wg-pyutils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
