import setuptools

print(setuptools.find_packages())
# exit()


with open("README.md", "r") as fh:
    long_description = fh.read()
 
setuptools.setup(
    name="dmp-player",
    version="1.0.0",
    author="Lam Kha Tinh",
    author_email="tinh.lkha@dmprof.com",
    description="Player video application",
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
        # If any package contains *.pyc files, include them:
        "": ["*.pyc", "*.py", "*.png"],
        # And include any *.msg files found in the "resources" package, too:
        "Play_Video_Script": ["resources/icons/*.png"],
    },
    entry_points={
        'console_scripts': [
            'dmp-player = Play_Video_Script.app:main',
        ],
    },
)