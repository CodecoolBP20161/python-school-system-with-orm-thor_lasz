import psycopg2
import getpass


def runSql(query):
    try:
        conn = psycopg2.connect(dbname=str(getpass.getuser()), user=str(getpass.getuser()))
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print("Uh oh, can't connect. Invalid dbname, user or password?")
        print(e)


if (__name__ == "__main__"):
    print(runSql("SELECT * FROM applicant"))
