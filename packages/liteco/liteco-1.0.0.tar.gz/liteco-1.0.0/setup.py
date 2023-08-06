from setuptools import setup

setup(
    name="liteco",
    version="1.0.0",
    description="A simple Python program to add colors to your terminal application",
    url="https://primidac@bitbucket.org/primidac/liteco.git",
    author="Primidac",
    author_email="primidac@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["liteco"],
    include_package_data=True,
    install_requires=["os"],
    entry_points={
        "console_scripts": [
            "liteco=liteco.__main__:main",
        ]
    },
)