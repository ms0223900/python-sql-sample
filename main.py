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
UPDATE_SQL = 'UPDATE abc SET title = ?, name = ? WHERE id = ?'

QUERY_SQL_BY_DATETIME = 'SELECT * FROM abc WHERE created_time > ?'
QUERY_SQL_RECENT_MONTH = 'SELECT * FROM abc WHERE created_time > DATE_ADD(CURRENT_DATE, INTERVAL -30 DAY) AND CURRENT_DATE'
# QUERY_SQL_RECENT_MONTH = 'SELECT * FROM abc WHERE created_time > DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY) AND CURRENT_DATE'
# QUERY_SQL_RECENT_MONTH = 'SELECT * FROM abc WHERE created_time = CURRENT_DATE'

DELETE_SQL = 'DELETE FROM abc WHERE id = ?'
DELETE_ALL_SQL = 'DELETE FROM abc'

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


def query_sql(conn: mariadb.Connection, sql=QUERY_SQL):
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()


def query_sql_by_datetime(conn: mariadb.Connection, created_at: str):
    cur = conn.cursor()
    cur.execute(QUERY_SQL_BY_DATETIME, [created_at])
    return cur.fetchall()

# add new rows to the database


def add_new_col(conn: mariadb.Connection, title: str, name: str):
    cur = conn.cursor()
    try:
        cur.execute(INSERT_SQL, [title, name])
    except mariadb.Error as e:
        print(f"Add dara to mariadb error: {e}")


def add_new_col_by_input():
    title = input("Enter title: ")
    name = input("Enter name: ")

    add_new_col(conn, title, name)


def update_col(conn: mariadb.Connection, id: int, title: str, name: str):
    cur = conn.cursor()
    try:
        cur.execute(UPDATE_SQL, [title, name, id])
    except mariadb.Error as e:
        print(f"Update database error: {e}")


def update_multi_col(conn: mariadb.Connection, args: list):
    cur = conn.cursor()
    try:
        cur.executemany(UPDATE_SQL, args)
    except mariadb.Error as e:
        print(f"Update database error: {e}")


def delete_table(conn: mariadb.Connection):
    cur = conn.cursor()
    try:
        cur.execute(DELETE_SQL)
    except mariadb.Error as e:
        print(f"Delete database error: {e}")


def input_single_col():
    id = int(input("Enter id: "))
    title = input("Enter title: ")
    name = input("Enter name: ")

    # return 順序很重要
    return (title, name, id)


def input_multi():
    res = []
    question = 'Do you want to continue? [y/n](press Enter to not continue)'

    while True:
        # 至少輸入一組
        input_res = input_single_col()
        res.append(input_res)

        input_answer = input(question).lower()
        if (input_answer == 'n' or bool(input_answer) is False):
            break

    return res


def main():
    # input_multi_res = input_multi()

    # update_multi_col(conn, input_multi_res)

    # add_new_col_by_input()
    # datetime = input('從什麼時候開始？')
    # queried = query_sql_by_datetime(conn, datetime)

    # delete_table(conn)

    queried = query_sql(conn, QUERY_SQL_RECENT_MONTH)
    print(queried)
    for (item) in queried:
        print(item)

    if (type(conn) is mariadb.Connection):
        conn.commit()  # commit to changes
        conn.close()  # close the connection


main()
