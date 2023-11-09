from private_details import *
from mariadb import connect
from mariadb import Error as MariaDBError
from mariadb.connections import Connection


def _get_connection() -> Connection:
    return connect(
        user=my_username,
        password=my_password,
        host=my_host,
        port=3306,
        database='job_match'
    )


def read_query(sql: str, sql_params=()):
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)

        return list(cursor)


def insert_query(sql: str, sql_params=()) -> int:
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)
        conn.commit()

        return cursor.lastrowid


def update_query(sql: str, sql_params=()) -> bool:
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)
        conn.commit()

        return cursor.rowcount > 0


def insert_transaction_across_tables(sql_queries: tuple[str], sql_params: tuple[tuple]):
    with _get_connection() as conn:
        insertion_indices = []
        try:
            cursor = conn.cursor()
            for i in range(len(sql_queries)):
                cursor.execute(sql_queries[i], sql_params[i])
                insertion_indices.append(cursor.lastrowid)
            conn.commit()
            return insertion_indices
        except MariaDBError as error:
            print(f"Insertion cascade failed: {error}")
            conn.rollback()
            return insertion_indices
