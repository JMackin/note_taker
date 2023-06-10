import os.path
from urllib import parse
import psycopg2
import sqlalchemy as sql


class DBAgent:

    def __init__(self):
        db_info_dict, auth_info_dict = conf()

        self.db_conn = self.build_connection(db_info_dict, auth_info_dict)

    def build_connection(self, db_info_dict: dict, auth_info_dict: dict):
        db_conn = \
            sql.create_engine(""
             f"postgresql+pyscopg2://"
             f"{auth_info_dict.get('username')}:"
             f"{parse.quote_plus(auth_info_dict.get('password'))}@"
             f"{db_info_dict.get('socket')}:"
             f"{db_info_dict.get('port')}/"
             f"{db_info_dict.get('database')}")

        self.db_conn = db_conn
        return db_conn


def conf():
    db_params = ('database', 'socket', 'port')
    auth_params = ('username', 'password')
    if os.path.exists(os.fspath(".jlmnotes-db_conf")):
        with open(".jlmnotes-db_conf") as con_str:
            con_info = str(con_str.read(())).splitlines()
            auth_info = con_info[1].split(":")
            db_info = con_info[0].split(":")

            try:
                db_param_dict = {k: v for k, v in zip(db_params, db_info)}
            except Exception as e:
                print(f"{e.with_traceback()}"
                      "\n Database info didnt parse"
                      "\n Connection config may not be formatted correctly.\n"
                      "\n please check .jlmnotes-db_conf\n"
                      "\n syntax:\n"
                      "<database>:<socket>:<port>\n"
                      "<username>:<password>\n\n")
                exit(1)

            try:
                auth_param_dict = {k: v for k, v in zip(auth_params, auth_info)}
            except Exception as e:
                print(f"{e}"
                      "\n Authentication info didnt parse"
                      "\n Connection config may not be formatted correctly."
                      "\n please check .jlmnotes-db_conf\n"
                      "\n syntax:\n"
                      "<database>:<socket>:<port>\n"
                      "<username>:<password>\n\n")
                exit(1)

        return db_param_dict, auth_param_dict

    else:
        print("\nConnection info file not found\n")
        print("Please set connection info in 'NoteTaker/.jlm-db_conf'\n")
        print("with format: \n\n"
              "     <database>:<socket>:<port>\n"
              "     <username>:<password>\n\n")
        exit(1)

