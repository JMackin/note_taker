import handle_gpg
import os
import psycopg

# INIT DB CONNECTION AND GET CONN OBJECT
def make_connection(db_name: str, usr: str):

    # connect to existing db
    with psycopg.connect(f'dbname={db_name} user={usr}') as conn:
        # open cursor for db ops
        return conn


# PARMS (PARAMETER) MUST BE TUPLE OR DICT
def execute_query(conn, query: str, parms=None):

    with conn.cursor() as cur:
        if parms is not None:
            cur.execute(query, parms)
        else:
            cur.execute(query)

def make_table(columns: list(dict), prim_key=None, foreign_keys=None, col_options=None):

    table_def = []

    for dtype, col in columns:


        table_def.append(f"{dtype} {col}")
