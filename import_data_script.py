import glob
import pypyodbc as odbc # pip install pypyodbc
import pandas as pd # pip install pandas

dj = pd.concat(map(pd.read_json, glob.glob('json/*.json')))
df = pd.concat(map(pd.read_csv, glob.glob('CSV/*.csv')))

dn = pd.concat((dj,df))

dn.drop(dn.query('date.isnull() | abbreviation_canton_and_fl.isnull() | ncumul_conf.isnull()').index, inplace=True)

columns = ['date', 'abbreviation_canton_and_fl', 'ncumul_conf']

dn_data = dn[columns]

records = dn_data.values.tolist()

DRIVER = 'SQL Server'
SERVRE_NAME = 'DESKTOP-JEAC83G\SQLEXPRESS'
DATABASE_NAME = 'CovidAppDB'

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
    INSERT INTO Swiss_Covid_Data
    VALUES (?, ?, ?)
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