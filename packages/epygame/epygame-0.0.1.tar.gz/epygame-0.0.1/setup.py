import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="epygame",
    version="0.0.1",
    author="Ethosa",
    author_email="ethosa.pygame@gmail.com",
    description="A library for Python using android classes based on the pygame library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ethosa/epygame",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pygame',
        "requests"
    ]
)