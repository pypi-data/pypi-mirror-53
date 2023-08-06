import psycopg2

conn = psycopg2.connect(
  dbname="dev",
  host="redshift-cluster-1.ctaozttcgvye.eu-central-1.redshift.amazonaws.com",
  port=5439,
  user="awsuser",
  password="P1n4p1n4"
)

cur = conn.cursor()

cur.execute("""SELECT 1""")
rows = cur.fetchall()
print(rows)
cur.close()
conn.close()
