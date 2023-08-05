import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hyperdim",
    version="0.0.6",
    description="Hyperdimensionality computing machine learning library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/da_doomer/hyperdim",
    packages=setuptools.find_packages(),
    install_requires=[
        'tqdm',
        'numpy',
        'sklearn',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
