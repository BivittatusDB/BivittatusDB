from setuptools import setup, find_packages

setup(
    name="BivitattusDB",
    version="2.1.0",
    author="HarbingerOfFire",
    author_email="harbingeroffire@proton.me",
    description="BivitattusDB",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/HarbingerOfFire/bivittatusDB",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    python_requires='>=3.8',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
