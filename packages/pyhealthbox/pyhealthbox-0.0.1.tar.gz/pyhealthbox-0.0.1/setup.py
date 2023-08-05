from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pyhealthbox",
    version="0.0.1",
    description="Python Client to interact with the Renson Healthbox 3.0 Ventilation system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sdiepend/pyhealthbox",
    author="Stijn Diependaele",
    author_email="sdiepend@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Home Automation",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    keywords="client api library renson healthbox ventilation",
    project_urls={
        "Documentation": "https://github.com/sdiepend/pyhealthbox/blob/master/README.md"
    },
    py_modules=["healthbox"],
    install_requires=[
        "requests"
    ],
    python_requires=">=3.5",
)