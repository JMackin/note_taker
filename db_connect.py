import psycopg
from psycopg import sql
import handle_gpg as hgpg


# INIT DB CONNECTION AND GET CONN OBJECT
def make_connection(db_name: str, usr: str):

    passwd_file = f'keys/{usr}_passwd.asc'
    passwd = hgpg.decrypt_it(passwd_file)

    # connect to existing db
    with psycopg.connect(conninfo=f"host=localhost port=5432 dbname={db_name} user={usr} password={passwd.data.decode('ascii')}") as conn:
        # open cursor for db ops
        print(conn.info.status)
        print(f"{conn.info.user}@{conn.info.host} on {conn.info.dbname}")



# PARMS (PARAMETER) MUST BE TUPLE OR DICT
# PARAMETERS ARE PASSED INTO PLACEHOLDER TAGS ( "%s" ) IN THE QUERY STRING
def execute_query(conn, query: str, parms=None):

    with conn.cursor() as cur:
        if parms is not None:
            cur.execute(query, parms)
        else:
            cur.execute(query)


# PARAMETERS:
#   columns : list[dict{}] i.e [{'col_name':'data_type'},{...}]
#   prim_key : str
#   foreign_keys : dict{}
#   col_options : dict{key:list[]} i.e. {"col_name": ['opt1', 'opt2', ...]}
def make_table(columns: list[dict], tabl_name: str, prim_key=None, foreign_keys=None, col_options=None):

    for i in columns:
        for cn, dt in i:
            if cn in col_options.keys():
                for opt in col_options[cn]:
                    dt = f"{dt} {opt}"
            if cn in foreign_keys.keys():
                dt = f"{dt} {foreign_keys[cn]}"
            if prim_key == cn:
                dt = f"{dt} PRIMARY KEY"

    tabl = sql.SQL("""
        CREATE TABLE {tabl_name} (
            {full_col}
        );""")\
        .format(
        tabl_name=tabl_name,
        full_col=sql.SQL(', ').join([sql.Composed(f"{sql.Identifier(cn)} {dt}") for i in columns for cn, dt in i]))

