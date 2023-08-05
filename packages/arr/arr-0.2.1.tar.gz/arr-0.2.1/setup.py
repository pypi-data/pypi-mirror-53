import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    requirements = fh.read().splitlines()

setuptools.setup(
    name="arr",
    version="0.2.1",
    author="Marco Müllner",
    author_email="muellnermarco@gmail.com",
    description="Astronomic Reference Resolver",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/muma7490/ARR",
    install_requires=requirements,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts':['arr = arr.__main__:main']
    }
)
