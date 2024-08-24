<p align="center">
<img src="./logo.png" />
</p>

[![Static Badge](https://img.shields.io/badge/Version-View-%20green)](./version.txt "1.1.0.5")
[![Static Badge](https://img.shields.io/badge/PIP%20-%20View-blue)](https://pypi.org/project/bivittatusDB/)
![Static Badge](https://img.shields.io/badge/MajorBuild-1.1.0.5-%20green)
![Static Badge](https://img.shields.io/badge/Language%20-%20Python%20(3.x)-blue)



# BivittatusDB: Operator-Based Relational Database Management System

This is a Python-based relational database management system (RDBMS) designed from scratch with operator-based functionalities. It's a standalone system not compatible with SQL or NoSQL databases, aiming to provide a simple yet functional database management solution.

## Features
- **Operator-based operations**: The database operates using operators such as `+`, `-`, and `==` to manipulate data.
- **Relational Structure**: Organizes data in tables with rows and columns, following a relational database model.
- **Basic CRUD Operations**: Supports basic Create, Read, Update, and Delete operations.
- **Indexing**: Efficient data retrieval with indexing mechanisms.
- **Transaction Management**: Implements transaction management to ensure data consistency.
- **Security**: All databases are asymmetrically encrypted with a user defined password for each database.

## Installation
Installation is now available through pip, via the latest release. To get the latest fix (with beta features) use
```bash
pip install bivittatusDB
```
The last build is unavailable at this time. Based on the [release schedule](https://github.com/HarbingerOfFire/bivittatusDB/wiki/dbed-0001), release 2.0.0.0 should be released 08/01/2025. The closest working version of build 1.0.0.0 available on PyPi is v1.0.0.1
```bash
pip install bivittatusDB==1.0.0.1
```

## Examples
See the examples directory and [wiki](https://github.com/HarbingerOfFire/PYDB/wiki) for examples off different operations.

## Usage
1. clone the repo and cd into the BivitattusDB directroy
2. Import bivittatusDB into your python file/interpreter.
3. Follow the information from the [wiki](https://github.com/HarbingerOfFire/PYDB/wiki) for more info on specific usage

## Dependencies
The databases are saved in hybrid-asymmetrically encrypted and therefore need encryption handlers, as seen in the [`requirements.txt`](.github/requirements.txt) file.
```bash
pip install -r .github/requirements.txt
```

## Contributing
Contributions are welcome! If you'd like to contribute to the project, please fork the repository and submit a pull request with your changes.See [Contributing](.github/CONTRIBUTING.md) & [Code of Cunduct](.github/CODE_OF_CONDUCT.md)

## License
This project is licensed under the [MIT License](.github/LICENSE).

This README.md file provides an overview of the operator-based relational database management system implemented in Python, detailing its current features, future plans, usage instructions, dependencies, and contribution guidelines. Additionally, it outlines the licensing information for the project.

## Known Issues: 
Due to recent updates, no issues are known at this time. All example files are acting as expected. We are accepting issues if you find anything that we have missed.
