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

        conn.commit()


def get_table_info(conn, tabl_name: str):

    query = sql.SQL("""
        SELECT column_name, data_type FROM information_schema.columns
        WHERE table_schema = 'public'
        AND table_name = {table}
    """)\
        .format(
        table=sql.Literal(tabl_name)
        )

    return execute_query(conn, query, return_result=True)


# REQUIRES THE USER-DEFINED FUNCTION get_pkey BE DEFINED
def get_prime_key_col(conn, tabl_name: str):

    query = sql.SQL("""
        SELECT * from get_pkey({table})
        """)\
        .format(
            table=sql.Literal(tabl_name)
        )

    pkey_result = execute_query(conn, query, True)

    return str(pkey_result[0][0])


def select_by_id(conn, tabl_name, record_id, column_names: list[str] = None):

    pkey = get_prime_key_col(conn, tabl_name)
    q = make_select_by_id(tabl_name, record_id, pkey, column_names)

    result = execute_query(conn, q, True)

    return result


def make_simple_insert(tabl_name: str, values: list, columns: list = None):

    if columns is not None:
        query = sql.SQL("""
                INSERT INTO {table} ({}) VALUES ({}) 
            """) \
            .format(
                sql.SQL(', ').join(map(sql.Identifier, columns)),
                sql.SQL(', ').join(map(sql.Literal, values)),
                table=sql.Identifier(tabl_name)
        )
    else:
        query = sql.SQL("""
            INSERT INTO {table} VALUES ({}) 
        """)\
            .format(
                sql.SQL(', ').join(map(sql.Literal, values)),
                table=sql.Identifier(tabl_name)
            )

    return query


def make_select_by_id(tabl_name: str, record_id: str, pkey_colname: str, column_names: list[str] = None):


    if column_names is not None:
        query = sql.SQL("""
              SELECT {columns} FROM {table}
              WHERE {pkey_column} = {id}
            """)\
            .format(
                columns=sql.SQL(', ').join(map(sql.Identifier, column_names)),
                table=sql.Identifier(tabl_name),
                pkey_column=sql.Identifier(pkey_colname),
                id=sql.Literal(record_id)
            )
    else:
        query = sql.SQL("""
                     SELECT * FROM {table}
                     WHERE {pkey_column} = {id}
                   """) \
            .format(
            table=sql.Identifier(tabl_name),
            pkey_column=sql.Identifier(pkey_colname),
            id=sql.Literal(record_id)
        )

    return query


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

