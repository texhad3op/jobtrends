import psycopg2

try:
    conn = psycopg2.connect("dbname='jobtrends' user='postgres' host='localhost' password='postgres'")
    print "Opened database successfully"

    cur = conn.cursor()

    cur.execute("SELECT vals from sites")
    rows = cur.fetchall()
    for row in rows:
        print "ID = ", row[0]

    print "Operation done successfully";
    conn.close()

except:
    print "I am unable to connect to the database"