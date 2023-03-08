import psycopg
from psycopg import sql
import handle_gpg as hgpg


# INIT DB CONNECTION AND GET CONN OBJECT
def make_connection(db_name: str, usr: str):

    passwd_file = f'keys/{usr}_passwd.asc'
    passwd = hgpg.decrypt_it(passwd_file)

    # connect to existing db
    conn = psycopg.connect(conninfo=f"host=localhost port=5432 dbname={db_name} user={usr} password={passwd.data.decode('ascii')}")
    del passwd
    # open cursor for db ops
    print(conn.info.status)
    print(f"{conn.info.user}@{conn.info.host} on {conn.info.dbname}")

    return conn


# PARMS (PARAMETER) MUST BE TUPLE OR DICT
# PARAMETERS ARE PASSED INTO PLACEHOLDER TAGS ( "%s" ) IN THE QUERY STRING
def execute_query(conn, query: str, return_result: bool = False, parms=None):

    with conn.cursor() as cur:
        if parms is not None:
            cur.execute(query, parms)
        else:
            cur.execute(query)

        # RETURN ALL RESULTS AS TUPLE (OR LIST?)
        if return_result:
            return cur.fetchall()


# PARAMETERS:
#   columns : dict{}
#   prim_key : str
#   foreign_keys : dict{}
#   col_options : dict{key:list[]} i.e. {"col_name": ['opt1', 'opt2', ...]}
def make_table(columns: dict, tabl_name: str, prim_key: str = None, foreign_keys: dict = None, col_options: dict = None):

    # COLUMN DEFINITION CONSTRUCTION
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

    # TABLE DEFINITION CONSTRUCTION
    tabl = sql.SQL("""
        CREATE TABLE {table} (
            {full_col}
        )""")\
        .format(
        table=sql.Identifier(tabl_name),
        full_col=sql.SQL(', ').join([sql.Composed([sql.Identifier(cn), sql.SQL(f" {dt}")]) for cn, dt in columns.items()])
        )

    return tabl


def get_table_info(conn, tabl_name: str):

    query = sql.SQL("""
        SELECT column_name FROM information_schema.columns
        WHERE table_schema = 'public'
        AND table_name = {table}
    """)\
        .format(
        table=sql.Literal('testtbl1')
        )

    return execute_query(conn, query, return_result=True)


def make_insert():
    print("TODO")