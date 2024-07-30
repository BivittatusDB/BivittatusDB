from setuptools import setup, find_packages

# Read the contents of the README file
with open("README.md", "r") as fh:
    long_description = fh.read()

with open(".github/requirements.txt", "r") as fh:
    depend=[]
    for line in fh:
        print(line)
        depend.append(line.strip()[3:])

setup(
    name="bivittatusDB",
    version="1.0.0.0",  # Update with the appropriate version
    author="HarbingerOfFire",
    author_email="harbingeroffire@proton.me",  # Replace with the author's email
    description="Operator Based Relational Database Management system for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HarbingerOfFire/bivittatusDB",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.x",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent?",
    ],
    python_requires='>=3.6',
    install_requires=depend,
)
