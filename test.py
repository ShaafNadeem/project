from typing import Any
import pyodbc
import pandas as pd
from configparser import ConfigParser
import urllib
from sqlalchemy import create_engine

class DataBaseReader():
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



class PreProcessor():
    def __init__(self) -> None:
        pass

    DataBaseReader.notes.rename(columns = {"Patient ID":"PatientID"}, inplace=True, )
    DataBaseReader.vitals['PatientID'] = DataBaseReader.vitals['PatientID'].astype(int)
    merged =  DataBaseReader.vitals.merge( DataBaseReader.notes, on = 'PatientID', how = 'inner')

class VitalsProducer():
    def __init__(self, PatientID:int):
        self.PatientID = PatientID

    def vitalsproduce(self):
        self.patientvitals = PreProcessor.merged[PreProcessor.merged['PatientID']==self.PatientID]




vitals = VitalsProducer(1122)
print(vitals)
    









class DataReader():
    db_name = 'One Practice Sample'
    server = 'CMDLHRDB01'
    database = 'One Practice Sample'
    trusted_connection = 'yes'  # Use Windows authentication
    driver = '{SQL Server}'

    def getData(self,table_name):
        connection_string = f"DRIVER={self.driver};SERVER={self.server};DATABASE={self.database};TRUSTED_CONNECTION={self.trusted_connection}"
        connection = pyodbc.connect(connection_string)
        data = pd.read_sql(f"select * from [One Practice Sample ].[dbo].[{table_name}]", connection)
        connection.close()
        return data
    
    def getFilteredData(self, table_name, columns):
        connection_string = f"DRIVER={self.driver};SERVER={self.server};DATABASE={self.database};TRUSTED_CONNECTION={self.trusted_connection}"
        connection = pyodbc.connect(connection_string)
        clns = "".join([f"[{col}]," for col in columns])
        clns = clns[:-1]
        data = pd.read_sql(f"select {clns} from [One Practice Sample ].[dbo].[{table_name}]", connection)
        connection.close()
        return data
    
    
class Preprocessor():
    og_column = "Patient ID"
    column_fixed = "PatientID"
    datatype = int
    def __init__(self, df):
        self.df = df
        

    
    def getRename(self, table_name):
        table_name.rename(columns = {self.og_column:self.column_fixed}, inplace=True, )
        return table_name
    
    def fixDatatype(self, table_name):
        table_name[self.column_fixed] = table_name[self.column_fixed].astype(self.datatype)
        return table_name
    

    

class InfoProducer(PreProcessor):
    def __init__(self, df):
        super().__init__(df=df)
        self.df = df
        self.df = super().getRename(table_name=self.df)
        self.df = super().fixDatatype(table_name=self.df)
    
    def __init__(self, patient_ID:int, merged):
        self.patient_ID = patient_ID
        self.merged = merged

        merged[merged['PatientID']==patient_ID]

    
    def getMerge(self, info1, info2):
        self.merged = table_name.merge(table_name2, on = self.column_fixed, how = 'inner')
        return self.merged
    
        
info1 = InfoProducer()
