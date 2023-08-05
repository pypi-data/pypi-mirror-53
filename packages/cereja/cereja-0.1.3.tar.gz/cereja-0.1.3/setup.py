import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

EXCLUDE_FROM_PACKAGES = ('cereja.tests'
                         )

setuptools.setup(
    name="cereja",
    version="0.1.3",
    author="Joab Leite",
    author_email="jlsn1@ifal.edu.br",
    description="My Utils",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jlsneto/cerejeira",
    packages=setuptools.find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)