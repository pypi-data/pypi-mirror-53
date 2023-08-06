import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="rapid-utils",
    version="0.0.3",
    description="high level functions",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/gnaam/rapid-utils",
    download_url="https://github.com/gnaam/rapid-utils/archive/0.0.3.tar.gz",
    author="Namdev Gavle",
    author_email="gavlenamdevprabha@gmail.com",
    license="MIT",
    packages=find_packages(),
    install_requires=["requests==2.22.0"],
    include_package_data=True,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5'
    ]
)