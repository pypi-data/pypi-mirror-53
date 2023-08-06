import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="passgenerate",
    version="0.0.3",
    author="Erdem Aybek",
    author_email="eaybek@gmail.com",
    description=" ".join(["Nothing"]),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eaybek/passgenerate",
    packages=setuptools.find_packages(),
    scripts=["bin/passgenerate"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Development Status :: 1 - Planning",
    ],
    install_requires=["exposer", "passgenerate"],
    python_requires=">=3.6",
)
