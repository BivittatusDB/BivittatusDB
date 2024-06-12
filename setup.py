from setuptools import setup

setup(
    name="BivitattusDB",
    version="2.1.0",
    author="HarbingerOfFire",
    author_email="harbingeroffire@proton.me",
    description="BivitattusDB",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/HarbingerOfFire/bivittatusDB",
    py_modules=["bdb_aggregate", "BDB_io", "BDB_metadata", "BDB_tb", "BivitattusView", "BivittatusDB", "metaclass"],
    package_dir={'': 'src'},
    python_requires='>=3.8',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
