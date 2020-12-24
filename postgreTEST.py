import psycopg2

con = psycopg2.connect(
  database="BlogDB",
  user="postgres",
  password="Qwe123",
  host="127.0.0.1",
  port="5432"
)

print("Database opened successfully")