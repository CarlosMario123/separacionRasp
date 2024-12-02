import os

class Config:
    DATABASE = os.getenv('DATABASE', 'data.db')
    AWS_RECORD_URL = os.getenv('AWS_RECORD_URL', 'https://100.24.202.224/record')
    AWS_TABLE_URL = os.getenv('AWS_TABLE_URL', 'https://100.24.202.224/table')
    DEBUG = os.getenv('DEBUG', True)
