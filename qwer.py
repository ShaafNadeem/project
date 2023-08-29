class DataReader():
    db_name = 'One Practice Sample'

    server = 'CMDLHRDB01'

    database = 'One Practice Sample'

    trusted_connection = 'yes'  # Use Windows authentication

    driver = '{SQL Server}'

    # def make_connection(self):

    #     connection_string = f"DRIVER={self.driver};SERVER={self.server};DATABASE={self.database};TRUSTED_CONNECTION={self.trusted_connection}"

    #     connection = pyodbc.connect(connection_string)

    def get_data(self, table_name):
        connection_string = f"DRIVER={self.driver};SERVER={self.server};DATABASE={self.database};TRUSTED_CONNECTION={self.trusted_connection}"

        connection = pyodbc.connect(connection_string)

        data = pd.read_sql(f"select * from [One Practice Sample ].[dbo].[{table_name}]", connection)

        connection.close()

        return data

    def get_filtered_data(self, table_name, columns):
        connection_string = f"DRIVER={self.driver};SERVER={self.server};DATABASE={self.database};TRUSTED_CONNECTION={self.trusted_connection}"

        connection = pyodbc.connect(connection_string)

        clns = "".join([f"[{col}]," for col in columns])

        clns = clns[:-1]

        print(clns)

        flns = "".join([f" [{col}] IS NOT NULL AND " for col in columns])

        flns = flns[:-4]

        print(flns)

        print(f"select {clns} from [One Practice Sample ].[dbo].[{table_name}] {flns}")

        data = pd.read_sql(f"select {clns} from [One Practice Sample ].[dbo].[{table_name}] WHERE{flns}", connection)

        connection.close()

        return data


class PreProcessor():
    og_column = "Patient ID"

    column_fixed = "PatientID"

    datatype = int

    def __init__(self, df):
        self.df = df

    def get_rename(self, table_name):
        table_name.rename(columns={self.og_column: self.column_fixed}, inplace=True, )

        return table_name

    def fix_datatype(self, table_name):
        table_name[self.column_fixed] = table_name[self.column_fixed].astype(self.datatype)

        return table_name


class InfoProducer(PreProcessor):

    def __init__(self, df):
        super().__init__(df=df)

        self.df = df

        self.df = super().get_rename(table_name=self.df)

        self.df = super().fix_datatype(table_name=self.df)

    # def __init__(self, patient_ID:int, merged):

    #     self.patient_ID = patient_ID

    #     self.merged = merged|

    # merged[merged['PatientID']==patient_ID]

    def merger(self, obj):
        merged = obj.df.merge(self.df, on='PatientID', how='inner')

        merged_obj = InfoProducer(merged)

        return merged_obj

    def index_link(self, index):  # to access data using index

        # id = self.df.iloc[index] #to find

        id = self.df.at[index, 'PatientID']  # info1.df.at[12, 'PatientID']

        # patient_id = self.df[self.df.PatientID==id] #patient_id = info1.df[info1.df.PatientID==6318]

        patient_id = self.df[self.df['PatientID'] == id]  # info1.df[info1.df['PatientID'] == 6318]

        return patient_id  # self.df[self.df['PatientID'] == patient_id]

    def get_id_data(self, id):  # to access data using id

        return self.df[self.df.PatientID == id]

    # def repeatlistpatient(self):

    #     self.df['Created Date and time'] = pd.to_datetime(self.df['Created Date and time']) #to extract the exact date and time

    # def latestdata(self):

    #     # self.df['Created Date and time'] = pd.to_datetime(self.df['Created Date and time']) #to extract the exact date and time

    #     return self.df.sort_values(by='Created Date And time',ascending=False)

# info1.df.sort_values(by='Created Date And time',ascending=False)

# info1.df['Created Date And time'] = pd.to_datetime(info1.df['Created Date And time'])

# info1.df.iloc[12]