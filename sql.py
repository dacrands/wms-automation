import os
import pyodbc


CONN_STR = r'Driver={{SQL Server}};Server={0};Database={1};UID={2};PWD={3};'.format(
    os.environ['WMS_GP_SERVER'],
    os.environ['WMS_GP_DB'],
    os.environ['WMS_GP_UID'],
    os.environ['WMS_GP_PWD']
)

COMPANY_QUERY = """
                SELECT [Vendor ID] as [Vendor Number] 
                    ,[Vendor Name] 
                    ,[Address 1] 
                    ,[Address 2] 
                    ,[City] 
                    ,[State] 
                    ,[Zip Code] FROM [SFRD].[dbo].[Vendors]
                WHERE [Vendor Class ID] NOT IN ('EMPLOYEE', 'LEGAL')
                """ 

conn = pyodbc.connect(CONN_STR)
cursor = conn.cursor()

cursor.execute(COMPANY_QUERY)

companies = []
row = cursor.fetchone() 
while row:     
    newCo = {
        'id': row[0],
        'name': row[1],
        'type': 'V',
        'address': row[2],
        'address2': row[3],
        'city': row[4],
        'state': row[5],
        'zipcode': row[6],
        'taxRate': '9'
    }
    companies.append(newCo)
    row = cursor.fetchone()

for co in companies:
    print(co)