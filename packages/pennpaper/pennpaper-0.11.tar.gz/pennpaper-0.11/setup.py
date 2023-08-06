import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


def get_requirements():
    with open("requirements.txt") as fp:
        return fp.read()

setuptools.setup(
    name="pennpaper",
    version="0.11",
    author="Ilya Kamenshchikov",
    author_email="ikamenshchikov@gmail.com",
    description="Set of utilities for ploting results of non-deterministic experiments, "
                "e.g. machine learning, optimization, genetic algorithms.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ikamensh/ilya_ezplot",
    packages=["pennpaper",
              "pennpaper.metric",
              "pennpaper.plot",
              "pennpaper.processing",],
    package_dir={'pennpaper': 'pennpaper'},
    python_requires=">=3.6",
    install_requires=get_requirements(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)