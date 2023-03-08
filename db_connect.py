import psycopg
from psycopg import sql
import handle_gpg as hgpg


# INIT DB CONNECTION AND GET CONN OBJECT
def make_connection(db_name: str, usr: str):

    passwd_file = f'keys/{usr}_passwd.asc'
    passwd = hgpg.decrypt_it(passwd_file)

    # connect to existing db
    conn = psycopg.connect(conninfo=f"host=localhost port=5432 dbname={db_name} user={usr} password={passwd.data.decode('ascii')}")
    # open cursor for db ops
    print(conn.info.status)
    print(f"{conn.info.user}@{conn.info.host} on {conn.info.dbname}")

    return conn



# PARMS (PARAMETER) MUST BE TUPLE OR DICT
# PARAMETERS ARE PASSED INTO PLACEHOLDER TAGS ( "%s" ) IN THE QUERY STRING
def execute_query(conn, query: str, parms=None):

    with conn.cursor() as cur:
        if parms is not None:
            cur.execute(query, parms)
        else:
            cur.execute(query)


# PARAMETERS:
#   columns : dict{}
#   prim_key : str
#   foreign_keys : dict{}
#   col_options : dict{key:list[]} i.e. {"col_name": ['opt1', 'opt2', ...]}
def make_table(columns: dict, tabl_name: str, conn, prim_key: str = None, foreign_keys: dict = None, col_options: dict = None):

    for cn, dt in columns.items():

        if col_options is not None:
            if cn in col_options.keys():
                for opt in col_options[cn]:
                    dt = f"{dt} {opt}"
                    columns[cn] = dt
        if foreign_keys is not None:
            if cn in foreign_keys.keys():
                dt = f"{dt} {foreign_keys[cn]}"
                columns[cn] = dt
        if prim_key == cn:
            dt = f"{dt} PRIMARY KEY"
            columns[cn] = dt

    tabl = sql.SQL("""
        CREATE TABLE {table} (
            {full_col}
        )""")\
        .format(
        table=sql.Identifier(tabl_name),
        full_col=sql.SQL(', ').join([sql.Composed([sql.Identifier(cn), sql.SQL(f" {dt}")]) for cn, dt in columns.items()]))

    with conn.cursor() as cur:
        cur.execute(tabl)
        conn.commit()


