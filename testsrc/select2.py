import psycopg2
import pprint as pp

try:
    conn = psycopg2.connect("dbname='jobtrends' user='postgres' host='localhost' password='postgres'")
    print "Opened database successfully"

    cur = conn.cursor()
    city = 'Vi%'
    cur.execute("SELECT name from city where name ilike %(name)s", {"name": city})
    rows = cur.fetchall()
    for row in rows:
        print "ID = ", row[0]
    conn.close()

except psycopg2.OperationalError:
    print "aaaaaaaaaaaaaa"
    print IndexError
except IndexError:
    print "bbbbbbbbbbbb"