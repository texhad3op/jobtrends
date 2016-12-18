import psycopg2
import pprint as pp

try:
    conn = psycopg2.connect("dbname='jobtrends' user='postgres' host='localhost' password='postgres'")
    print "Opened database successfully"

    cur = conn.cursor()
    cityp = "Kaunas"
    city = cityp[0:4] + '%'
    cur.execute("SELECT id from city where name ilike %(name)s", {"name": city})
    rows = cur.fetchall()
    # for row in rows:
    print "ID = ", rows[0][0]
    conn.close()

except psycopg2.OperationalError:
    print "aaaaaaaaaaaaaa"
    print IndexError
except IndexError:
    print "bbbbbbbbbbbb"