from setuptools import find_packages,setup


setup(
    name = 'tradingts', 
    version="0.0.4",
    author="ts_python_user",
    description="ts python package",
    long_description=open('README.md', 'r').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/",
    packages=find_packages(), 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)