import setuptools

setuptools.setup(
    name="pyrca",
    version="0.2.0",
    author="Alexius Sayco Academia",
    author_email="alexius.academia@gmail.com",
    description="Python package for analysis of concrete structures.",
    long_description_content_type="text/markdown",
    url="https://github.com/syncsoft-solutions/pyrca",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)