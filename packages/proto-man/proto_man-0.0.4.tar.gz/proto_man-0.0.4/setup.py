import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="proto_man",
    version="0.0.4",
    author="Surya Pradyumna",
    author_email="surya.pradyumna@vogo.in",
    description="Protobuf repositories",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vogolabs/proto-man",
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'protobuf>=3.8.0',
    ],
)