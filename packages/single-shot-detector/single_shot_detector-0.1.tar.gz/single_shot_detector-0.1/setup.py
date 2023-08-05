import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='single_shot_detector',  
    version='0.1',
    author="André Bargas",
    author_email="andrebargas@gmail.com",
    description="Implementação Generica de um single shot detector",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/javatechy/dokr",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
    