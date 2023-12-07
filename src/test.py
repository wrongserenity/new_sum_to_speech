import psycopg2

try:
    conn = psycopg2.connect(host='postgres:5432', database='postgres',
                            user='postgres', password='postgres')
except Exception as e:
    print(e)
    exit(0)

cur = conn.cursor()

sql = "SELECT * FROM parsed_url"

cur.execute(sql)
data = cur.fetchall()

conn.close()
print(data)
