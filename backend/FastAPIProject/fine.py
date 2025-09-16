from dotenv import load_dotenv
import os
load_dotenv()

MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_SERVER = '127.0.0.1'
MYSQL_PORT = 3306
MYSQL_DB = 'kanbango_db'


SqlAlchemy_DataBase_Url = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_SERVER}:{MYSQL_PORT}/{MYSQL_DB}'
print(SqlAlchemy_DataBase_Url)