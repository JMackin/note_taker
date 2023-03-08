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

# CLOSE CONNECTION
conn.close()
del conn
