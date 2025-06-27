
from datetime import timedelta
class Config:
    SQL_SERVER = 'YourServername'
    SQL_DATABASE = 'YourDbName'
    SQL_DRIVER = 'ODBC Driver 17 for SQL Server'

    SQLALCHEMY_DATABASE_URI = (
        f"mssql+pyodbc://@{SQL_SERVER}/{SQL_DATABASE}"
        f"?driver={SQL_DRIVER.replace(' ', '+')}&trusted_connection=yes"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = 'YourKey'
    JWT_SECRET_KEY = 'YourKey'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
