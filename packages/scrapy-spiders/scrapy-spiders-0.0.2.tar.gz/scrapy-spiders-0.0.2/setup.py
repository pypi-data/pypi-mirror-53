import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scrapy-spiders",
    version="0.0.2",
    author="quicksort",
    author_email="quicksort@outlook.com",
    description="Spiders for scrapy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/quick-sort/scrapy-spiders.git",
    install_requires=["xlrd", "scrapy"],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
