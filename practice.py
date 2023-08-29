from typing import Any
import pyodbc
import pandas as pd
from configparser import ConfigParser
import urllib
from sqlalchemy import create_engine

#############READING DATABASE#################


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

query = """Select [Patient ID], [Diagnosis Codes] FROM [One Practice Sample ].[dbo].[ProviderNotes]
 WHERE [Diagnosis Codes] IS NOT NULL"""

query2 = """SELECT [Server Name], [DBNAME], [Practice], [VitalsID], [Date/Time], [PatientID], [PatientFirstName], [PatientLastName], [Weight], [Height], [Waist], [Neck], [BMI], [BSA], [Category], [LeanBodyWeight], [IdealBodyWeight], [OxygenSaturation], [PeakExpiratoryFlow], [InspiredOxygenFraction], [BloodType], [BloodRh], [FingerStick], [SeverityofPain], [UrineOutput], [LatestRecord], [Pulse], [Respiration], [Temperature], [Systolic], [Diastolic], [NoteID], [CreateDate], [UpdateDate]
FROM [One Practice Sample].[dbo].[Vitals]"""

# Read data using the SQLAlchemy engine
notes = pd.read_sql(query, engine)
vitals = pd.read_sql(query2, engine)

# Close the connection
connection.close()
# print(notes, vitals)

################PREPROCESSING##########################


notes.rename(columns={"Patient ID": "PatientID"}, inplace=True, )
vitals['PatientID'] = vitals['PatientID'].astype(int)
merged = vitals.merge(notes, on='PatientID', how='inner')
# print(merged)

#######EXTRACTING VITALS################

PatientID = 1
patientvitals = merged[merged['PatientID'] == PatientID]


# print(patientvitals)


###############FILTERED_DATA###########################
def getFilteredData(table_name, columns):
    connection_string = f"DRIVER={driver};SERVER={server};DATABASE={database};TRUSTED_CONNECTION={trusted_connection}"
    connection = pyodbc.connect(connection_string)
    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus(connection_string)}")
    clns = "".join([f"[{col}]," for col in columns])
    clns = clns[:-1]
    data = pd.read_sql(f"select {clns} from [One Practice Sample ].[dbo].[{table_name}]", engine)
    connection.close()
    return data


selection = getFilteredData('Diagnosis',['ICD-10'])
print(selection)



