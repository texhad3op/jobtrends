import psycopg2
import datetime

try:
    conn = psycopg2.connect("dbname='jobtrends' user='postgres' host='localhost' password='postgres'")

    cur = conn.cursor()

    #     "time" timestamp without time zone,
    # "date" date,
    # jobtitle text,
    # hiring_organisation text,
    # job_location text,
    # url text

    # cur.execute(
    #     "INSERT INTO events (site, time, date, jobtitle, hiring_organisation, job_location, url) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id;",
    #     ("fffff", datetime.datetime.now(), datetime.datetime.now(), "abcdef", "hhhhhhhh", "kkkkkkkkkkk", "vvvvvvvvvvvv"))
    # hundred = cur.fetchone()[0]

    cur.execute("INSERT INTO city (name) VALUES ('%s') RETURNING id;" % ("fffff"))
    hundred = cur.fetchone()[0]

    print hundred
    conn.commit()
    cur.close()
    conn.close()
except ValueError:
    print ValueError
