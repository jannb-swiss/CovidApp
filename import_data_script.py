import glob
import pypyodbc as odbc
import pandas as pd

dj = pd.concat(map(pd.read_json, glob.glob('json/*.json')))
df = pd.concat(map(pd.read_csv, glob.glob('CSV/*.csv')))

dn = pd.concat((dj,df))

dn.drop(dn.query('iso_code.isnull() | continent.isnull() | location.isnull() | date.isnull() | total_cases.isnull()').index, inplace=True)

columns = ['iso_code', 'continent', 'location', 'date', 'total_cases']

dn_data = dn[columns]

records = dn_data.values.tolist()

DRIVER = 'SQL Server'
SERVRE_NAME = 'DESKTOP-JEAC83G\SQLEXPRESS' #dein server name
DATABASE_NAME = 'CovidAppDB' #dein database name

def connection_string(driver, server_name, database_name):
    conn_string = f"""
        DRIVER={{{driver}}};
        SERVER={server_name};
        DATABASE={database_name};
        Trust_Connection=yes;        
    """
    return conn_string

try:
    conn = odbc.connect(connection_string(DRIVER, SERVRE_NAME, DATABASE_NAME))
except odbc.DatabaseError as e:
    print('Database ERROR:')
    print(str(e.value[1]))
except odbc.Error as e:
    print('Connection Error:')
    print(str(e.value[1]))

sql_insert = '''
    INSERT INTO Covid_Data_Country(ISO_Code, Kontinent, Land, Datum)
    VALUES (?, ?, ?, ?)
    INSERT INTO Covid_Data_Cases(Total_Ansteckungen)
    VALUES (?)
'''

try:
    cursor = conn.cursor()
    cursor.executemany(sql_insert, records)
    cursor.commit();
except Exception as e:
    cursor.rollback()
    print(str(e[1]))
finally:
    print('Die Daten sind in der Datenbank! :)')
    cursor.close()
    conn.close()