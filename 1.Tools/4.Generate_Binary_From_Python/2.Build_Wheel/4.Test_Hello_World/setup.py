import setuptools

print(setuptools.find_packages())
# exit()


with open("README.md", "r") as fh:
    long_description = fh.read()
 
setuptools.setup(
    name="test-hello",
    version="1.1.0",
    author="Lam Kha Tinh",
    author_email="tinh.lkha@dmprof.com",
    description="Wire detection package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True,
    package_data={
        # If any package contains *.pyc or *.rst files, include them:
        "": ["*.pyc", "*.rst"],
        # And include any *.msg files found in the "hello" package, too:
        "hello": ["*.msg"],
    },
    entry_points={
        'console_scripts': [
            'app = app.main:main',
        ],
    },
)