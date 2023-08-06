import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="beep-boop-test",
    version="0.1",
    author="David Eduard",
    author_email="edyalex.david@gmail.com",
    description="Beep? Boop!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EduardAlex/beepboop",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Public Domain",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)