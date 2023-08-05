import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="active_sample",
    version="0.0.2",
    author="Billy Su",
    author_email="g4691821@gmail.com",
    description="An active learning sampler",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/billy4195/active_sample",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    license='Apache License 2.0',
    data_files=[("", ["LICENSE"])]
)
