<p align="center">
<img src="./logo.png" />
</p>

![Static Badge](https://img.shields.io/badge/Version-2.0.0-%20green)
![Static Badge](https://img.shields.io/badge/Language%20-%20Python%20(3.12)-blue)
![Static Badge](https://img.shields.io/badge/Status%20-%20Intermediate%20-%20blue)


# BivittatusDB: Operator-Based Relational Database Management System (Stage Two)

This is a Python-based relational database management system (RDBMS) designed from scratch with operator-based functionalities. It's a standalone system not compatible with SQL or NoSQL databases, aiming to provide a simple yet functional database management solution.

## Features
- **Operator-based operations**: The database operates using operators such as `+`, `-`, and `==` to manipulate data.
- **Relational Structure**: Organizes data in tables with rows and columns, following a relational database model.
- **Basic CRUD Operations**: Supports basic Create, Read, Update, and Delete operations.
- **Indexing**: Efficient data retrieval with indexing mechanisms.
- **Transaction Management**: Implements transaction management to ensure data consistency. (Coming in Stage 3)

## Stage Two Implementation
At this stage, the database system supports the following features:
- Creating tables with specified columns.
- Inserting data into tables.
- Deleting data from tables.
- Basic querying using select operations.
- Table joins (right, left, and full)
- Autocommit
- Primary Keys (with integrity checks)
- Data typing (with integrity checks)

## Examples
See the examples directory for examples off different operations.

## Future Plans (Stage Three)
For the next stage of development, the following features are planned to be implemented:
- **Foreign Keys**: Establish relationships between tables to enforce referential integrity.
- **Update Values**: Implement functionality to update values directly instead of deleting and adding back.
- **Transaction Management**: Implement savepoints and rollback features to ensure consistency.
- **Data Compression**: Compress data to save space in files

## Usage
1. Import bivittatusDB into your python file/interpreter.
2. Follow the information from the [wiki](https://github.com/HarbingerOfFire/PYDB/wiki) for more info on specific usage

## Dependencies
The databases are saved in h5 files, and as such requires the h5py module, as seen in the [`requirements.txt`](./requirements.txt) file.
```bash
pip install -r requirements.txt
```

## Contributing
Contributions are welcome! If you'd like to contribute to the project, please fork the repository and submit a pull request with your changes.

## License
This project is licensed under the [MIT License](LICENSE).

This README.md file provides an overview of the operator-based relational database management system implemented in Python, detailing its current features, future plans, usage instructions, dependencies, and contribution guidelines. Additionally, it outlines the licensing information for the project.

# !!!UPDATE!!! STAGE 3 IN PROGRESS
Stage 3 is now in development, with the following changes scheduled to be made:
1. Transactional Management: add COMMIT and ROLLBACK features for transactional Management (Done: [22cb24f](https://github.com/HarbingerOfFire/bivittatusDB/commit/22cb24fd69e657ac9ca1c9818c69f5d37cb0adb8))
2. Foreign keys: Add foreign keys with proper refrencing and on update options (STARTED: [9ba4ac8](https://github.com/HarbingerOfFire/bivittatusDB/commit/9ba4ac8521493d290c6ee94c713dde8de9609bd9))
3. DATA Compression: data will be compressed before storing, to (hopefully) midigate the size of large databases. (Done: [4271d01](https://github.com/HarbingerOfFire/bivittatusDB/commit/4271d0175fc96e65dbda00bcbaffffbe131b14b1))
4. Change of Set-Item to change values instead of change column names (Done: [eeea1e0](https://github.com/HarbingerOfFire/bivittatusDB/commit/eeea1e05d84f5b940e08ce80b00457cffdf368b6))
5. Manual scan: if the raw data is updated, you can run a scan to check integrity
6. Finalizing of aggregate functions