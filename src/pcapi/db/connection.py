# Database connection wrapper

from pcapi import config, logtool

log = logtool.getLogger("connection", "pcapi")

use_sqlite = config.has_option("path", "sessionsdb")
if use_sqlite:
    # using sqlite
    #from pysqlite2.dbapi2 import OperationalError
    import pysqlite2.dbapi2 as db

    # full path of sqlite3 database
    db_path = config.get("path", "sessionsdb")
    log.info('Connect to sqlite using {0}'.format(db_path))

    # creating/connecting the test_db.
    # "check_same_thread" turns off some false alarms from sqlite3.
    # NOTE: mod_wsgi runs these global variables in *different* processes for each request.
    conn = db.connect(db_path, check_same_thread=False)
else:
    # try postgres
    import psycopg2
    db = 'dbname={0} user={1} password={2} host={3} port={4}'.format(
        config.get("pg", "database_database"),
        config.get("pg", "database_user"),
        config.get("pg", "database_password"),
        config.get("pg", "database_host"),
        config.get("pg", "database_port"))
    log.info('Connect to postgres using {0}'.format(db))
    conn = psycopg2.connect(db)

# token tables
TOKENS_TABLE = """
CREATE TABLE IF NOT EXISTS "tokens"\
  (id SERIAL PRIMARY KEY,\
   userid text unique,\
   reqsec text,\
   acckey text,\
   accsec text,\
   dt date default current_date);\
"""

TEMP_TABLE = """
CREATE TABLE IF NOT EXISTS "temp_request"\
  (userid text unique,\
   reqsec text );\
 """

c = conn.cursor()
c.execute(TOKENS_TABLE)
c.execute(TEMP_TABLE)
conn.commit()

#################
