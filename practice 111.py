from datetime import datetime
import urllib
import pyodbc
import pandas as pd
from sqlalchemy import create_engine

server = 'CMDLHRDB01'
database = 'One Practice Sample'
trusted_connection = 'yes'
driver = '{SQL Server}'

# Create a connection string for pyodbc
connection_string = f"DRIVER={driver};SERVER={server};DATABASE={database};TRUSTED_CONNECTION={trusted_connection}"

# Create a pyodbc connection
connection = pyodbc.connect(connection_string)

# Create an SQLAlchemy engine using the pyodbc connection
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus(connection_string)}")


def getFilteredData(table_name, columns):
    connection_string = f"DRIVER={driver};SERVER={server};DATABASE={database};TRUSTED_CONNECTION={trusted_connection}"
    connection = pyodbc.connect(connection_string)
    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus(connection_string)}")
    clns = "".join([f"[{col}]," for col in columns])
    clns = clns[:-1]
    data = pd.read_sql(f"select {clns} from [One Practice Sample ].[dbo].[{table_name}]", engine)
    connection.close()
    return data

# id = int(input('Enter your id:'))
#
#
# diagnosis_list = getFilteredData('Diagnosis', ['Patient ID','Description','Last Updated Date'])
# latest_dates_idx = diagnosis_list.groupby('Patient ID')['Last Updated Date'].idxmax()
# latest_diagnoses = diagnosis_list.loc[latest_dates_idx]
# latest_description = latest_diagnoses.loc[latest_diagnoses['Patient ID'] == id, 'Description'].squeeze()
# print(latest_description)


query = """
SELECT [PatientID], [CreateDate], [Weight], [Height], [Waist], [Neck], [BMI], [BSA], [Category], [LeanBodyWeight], [IdealBodyWeight], [OxygenSaturation], [PeakExpiratoryFlow], [InspiredOxygenFraction], [BloodType], [BloodRh], [FingerStick], [SeverityofPain], [UrineOutput], [LatestRecord], [Pulse], [Respiration], [Temperature], [Systolic], [Diastolic]
FROM [One Practice Sample].[dbo].[Vitals]
"""
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus(connection_string)}")

vitals = pd.read_sql(query, engine)
vitals['PatientID'] = vitals['PatientID'].astype(int)

# vitals = vitals[vitals['CreateDate'].str.match(r'[A-Za-z]{3} \d{1,2} \d{4} \d{1,2}:\d{2}[APap][Mm]')]
vitals['CreateDate'] = pd.to_datetime(vitals['CreateDate'], format='%b %d %Y %I:%M%p')
print(type(vitals['CreateDate'][5]))

filtered_sorted = vitals[vitals['PatientID'] == 7430].sort_values(by='CreateDate', ascending=False)
# print(filtered_sorted.iloc[0])
print(filtered_sorted.head(2))










