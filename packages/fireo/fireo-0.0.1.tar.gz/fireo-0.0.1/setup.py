from setuptools import setup

with open("README.md", "r") as fh:
    long_decription = fh.read()

setup(
    name='fireo',
    version='0.0.1',
    description='FireStore ORM',
    long_decription=long_decription,
    long_decription_content_type="text/markdown",
    url="https://github.com/octabytes/FireO.git",
    author="OctaByte",
    author_email="Dev@octabyte.io",
    py_modules=["helloworld"],
    package_dir={'': 'src'}
)