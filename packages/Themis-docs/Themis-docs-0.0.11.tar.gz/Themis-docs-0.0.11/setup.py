from setuptools import setup, find_packages


NAME = "Themis-docs"
DESCRIPTION = "Docs  template generator"
VERSION = "0.0.11"
REQUIRES_PYTHON = ">=3.6.0"
setup(
    name=NAME,
    version=VERSION,
    python_requires=REQUIRES_PYTHON,
    url="https://github.com/jetbridge/themis",
    license="ABRMS",
    author="JetBridge",
    author_email="adam@jetbridge.com",
    description=DESCRIPTION,
    long_description="",
    long_description_content_type="text/markdown",
    # py_modules=['jb'],
    # if you would be using a package instead use packages instead
    # of py_modules:
    packages=find_packages(exclude=["test", "*.test", "*.test.*", "test.*"]),
    zip_safe=False,
    include_package_data=True,
    platforms="any",
    install_requires=["jinja2", "sqlalchemy", "boto3", "pdfkit"],
)


