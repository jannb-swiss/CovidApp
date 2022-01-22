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

## Usage