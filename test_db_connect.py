import db_connect as dbconn

# OPEN CONNECTION
conn = dbconn.make_connection('dbajlm', 'dbajlm')


# tabl = dbconn.make_table({'id': 'integer', 'title': 'varchar(10)', 'date_did': 'date'},
#                   'testtbl1',
#                   prim_key="id",
#                   col_options={'title': ['NOT NULL', 'UNIQUE'], 'date_did': ['NOT NULL']}
#                   )
#
#
# # EXECUTE CONNECTION
# dbconn.execute_query(conn, tabl)

# print(dbconn.get_table_info(conn, 'testtbl1'))

# insert_query = dbconn.make_simple_insert('testtbl1', [8, "atitle", "now()"])
# dbconn.execute_query(conn, insert_query)
#
# print(dbconn.get_prime_key_col(conn, 'testtbl1'))

# q = dbconn.make_select_by_id('testtbl1', 6, 'id')

# print(dbconn.execute_query(conn, q, True))

print(dbconn.select_by_id(conn, 'testtbl1', 6, ["title", "date_did"]))

# CLOSE CONNECTION
conn.close()
del conn
