import psycopg2
import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()
  
conn = psycopg2.connect(
    host=os.environ.get('DB_HOST'),
    database=os.environ.get('DB_NAME'),
    port=os.environ.get('DB_PORT'),
    user=os.environ.get('DB_USER'),
    password=os.environ.get('DB_PASSWORD'))

# conn = psycopg2.connect(
#     host = "217.71.129.139",
#     port = "4580",
#     database = "postgres",
#     user = "postgres",
#     password = "postgres"  
# )

# conn = asyncpg.connect(
#     host = "217.71.129.139",
#     port = "4580",
#     database = "postgres",
#     user = "postgres",
#     password = "postgres" 
# )