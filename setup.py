import time

from setuptools import setup, find_packages


def generate_version():
    return time.strftime("0.1.%Y%m%d%H%M%S")


setup(
    name="jpipe-runner",
    version=generate_version(),
    author="Jason Lyu",
    author_email="xjasonlyu@gmail.com",
    description="A Justification Runner designed for jPipe",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/xjasonlyu/jpipe-runner",
    packages=find_packages(),
    install_requires=open("requirements.txt").read().splitlines(),
    python_requires=">=3.13",
    entry_points={
        "console_scripts": [
            "jpipe-runner = jpipe_runner.runner:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
