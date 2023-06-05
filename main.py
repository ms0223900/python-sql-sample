import mariadb
import sys

db_config = {
    "username": "root",
    "password": "",
    "host": "127.0.0.1",
    "port": 3306,
    "database": "test"
}

QUERY_SQL = 'SELECT * FROM (abc)'
INSERT_SQL = 'INSERT INTO abc (title, name) VALUES (?, ?)'

try:
    conn = mariadb.connect(
        user=db_config["username"],
        password=db_config["password"],
        host=db_config["host"],
        port=db_config["port"],
        database=db_config["database"]
    )
except mariadb.Error as e:
    print(f"Error connecting to mariadb {e}")
    sys.exit(1)

# read the database
def query_sql(conn: mariadb.Connection):
    cur = conn.cursor()
    cur.execute(QUERY_SQL)
    return cur.fetchall()

# add new rows to the database
def add_new_col(conn: mariadb.Connection, title: str, name: str):
    cur = conn.cursor()
    try:
        cur.execute(INSERT_SQL, [title, name])
    except mariadb.Error as e:
        print(f"Add dara to mariadb error: {e}")

def main():
    title = input("Enter title: ")
    name = input("Enter name: ")

    add_new_col(conn, title, name)

    queried = query_sql(conn)
    for (item) in queried:
        print(item)

    if(type(conn) is mariadb.Connection):
        conn.commit() # commit to changes
        conn.close() # close the connection

main()