from os import path

from setuptools import setup, find_namespace_packages


setup(
    name="montapy-core",
    version="0.3.0",
    description="Shared core for all montapy packages",
    long_description=open(path.join(path.dirname(__file__), "README.md")).read(),
    long_description_content_type="text/markdown",
    license="MIT",
    author="Sergey Volkov",
    author_email="volkov.sergey.e@gmail.com",
    package_dir={
        "": "src"
    },
    packages=find_namespace_packages(
        'src',
        include='montapu.*'
    ),
    extras_require={
        'test': [
            'pytest==5.1.3',
            'pytest-cov==2.7.1',
            'diff-cover==2.3.0'
        ],
        'dev': [
            'pylint==2.4.1',
            'pylint-quotes==0.2.1'
        ]
    },
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Framework :: AsyncIO",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development",
        "Topic :: Utilities"
    ]
)
