# Covid App

## Configuration

Create a config file `config.py` with the needed database configuration. See example:

```
db_credentials = dict(
    driver='{SQL Server}',
    host='localhost',
    database='CovidAppDB',
    user='',
    password=''
)
```

### *Note*:

Use correct driver based on you operating system:

* Windows: `{SQL Server}`
* macOS: `{ODBC Driver 17 for SQL Server}`

## Setup Database Schema

Before using the Python scripts to import and visualize data, you have to create the database schema.

Just run the SQL script on the MSSQL Server instance: `./sql/create-schema.sql`

## Usage

### Import data

```
python3 scripts/import_data.py [-v --verbose]
```

### Visualize data

```
python3 scripts/visualize_data.py
```