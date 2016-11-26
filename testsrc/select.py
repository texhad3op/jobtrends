import psycopg2
import pprint as pp

try:
    conn = psycopg2.connect("dbname='jobtrends' user='postgres' host='localhost' password='postgres'")
    print "Opened database successfully"

    cur = conn.cursor()

    cur.execute("SELECT id from city where name = %(name)s", {"name": 'Vilniuss'})
    rows = cur.fetchall()
    print("ID = ", rows[0][0])
    conn.close()

except psycopg2.OperationalError:
    print "aaaaaaaaaaaaaa"
    print IndexError
except IndexError:
    print "bbbbbbbbbbbb"
