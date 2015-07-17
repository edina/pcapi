"""
this script migrates FTGB pcapi tokens from sqlite to postgres
to run this activate the pcapi virtualenv
"""

import os

import pysqlite2.dbapi2 as db
import psycopg2

from pcapi import config
from pcapi.db import tokens

# sqllite db
pcapi_dir = os.path.join(os.environ['HOME'], '.pcapi',)
path = os.path.join(pcapi_dir, 'data', 'sessions.db')
sconn = db.connect(path)

# postgres
print config.get("pg", "database_database")
pg = 'dbname={0} user={1} password={2} host={3} port={4}'.format(
    config.get("pg", "database_database"),
    config.get("pg", "database_user"),
    config.get("pg", "database_password"),
    config.get("pg", "database_host"),
    config.get("pg", "database_port"))
pconn = psycopg2.connect(pg)

c = sconn.cursor()
c.execute('SELECT userid, reqsec, acckey, accsec, dt FROM tokens ORDER BY id')

INSERT = "INSERT INTO tokens(userid,reqsec,acckey,accsec,dt) SELECT %s,%s,%s,%s,%s WHERE NOT EXISTS (SELECT 1 FROM tokens WHERE userid = %s)"

for t in c.fetchall():
    pc = pconn.cursor()
    userid = t[0]
    print 'Migrating ', userid
    pc.execute(INSERT,  (userid, t[1], t[2], t[3], t[4], userid))
    pc.close()

print 'Done'
c.close()
sconn.close()

pconn.commit()
pconn.close()
