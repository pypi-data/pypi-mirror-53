import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="avro-object-furlan",
    version="0.0.3",
    author="Guionardo Furlan",
    author_email="guionardo@gmail.com",
    description="Helper class for (de)serialization of objects using Apache Avro",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/guionardo/py_avroobject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'fastavro',
        'requests'
    ],
    python_requires='>=3.6',
)
