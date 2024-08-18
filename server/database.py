import psycopg2

conn = psycopg2.connect(
    host="217.71.129.139",
    database="postgres",
    port = "4580",
    user="postgres",
    password="postgres")