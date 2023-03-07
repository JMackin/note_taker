import db_connect as dbconn

conn = dbconn.make_connection('dbajlm', 'dbajlm')
print(conn.info.error_message)
