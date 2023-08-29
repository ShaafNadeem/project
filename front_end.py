from flask import Flask, render_template, request
import urllib
import pyodbc
import pandas as pd
from sqlalchemy import create_engine

app = Flask(__name__)
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


def get_diagnosis(patient_id):
    diagnosis_list = getFilteredData('Diagnosis', ['Patient ID', 'Description', 'Last Updated Date'])
    latest_dates_idx = diagnosis_list.groupby('Patient ID')['Last Updated Date'].idxmax()
    latest_diagnoses = diagnosis_list.loc[latest_dates_idx]
    latest_description = latest_diagnoses.loc[latest_diagnoses['Patient ID'] == patient_id, 'Description'].squeeze()
    return latest_description


#


@app.route('/', methods=['GET', 'POST'])
def index():
    patient_id = None
    diagnosis = None
    if request.method == 'POST':
        patient_id = int(request.form['patient_id'])
        diagnosis = get_diagnosis(patient_id)
    if request.method == 'GET':
        diagnosis = None
    return render_template('try.html', diagnosis=diagnosis, patient_id=patient_id)


if __name__ == '__main__':
    app.run(debug=True)
