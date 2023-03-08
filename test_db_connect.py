import db_connect as dbconn

# OPEN CONNECTION
conn = dbconn.make_connection('dbajlm', 'dbajlm')
print("next")
dbconn.make_table({'id': 'integer', 'title': 'varchar(10)', 'date_did': 'date'},
                  'testtbl1',
                  conn,
                  prim_key="id",
                  col_options={'title': ['NOT NULL', 'UNIQUE'], 'date_did': ['NOT NULL']}
                  )

# CLOSE CONNECTION
conn.close()
del conn
