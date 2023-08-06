import setuptools

requirements = ["requests>=2.22.0"]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='conversus-api',
    version='0.0.1',
    author="Anthony Bu",
    author_email="abu@converseon.com",
    description="Python SDK for Conversus API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/converseon/conversus_sdk",
    packages=setuptools.find_packages(exclude="tests"),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements
)
