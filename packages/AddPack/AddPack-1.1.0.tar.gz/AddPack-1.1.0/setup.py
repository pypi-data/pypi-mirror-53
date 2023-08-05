import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="AddPack",
    version="1.1.0",
    author="Hema Negi",
    author_email="hemanegi444@gmail.com",
    description="A small add program package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hemanegi444/git_repository",
    packages=['AddPack'],
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
