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

print(dbconn.get_table_info(conn, 'testtbl1'))

insert_query = dbconn.make_simple_insert('testtbl1', [8, "atitle", "now()"])
dbconn.execute_query(conn, insert_query)

# CLOSE CONNECTION
conn.close()
del conn
