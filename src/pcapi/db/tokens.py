# -*- coding: utf-8 -*-

from connection import conn, use_sqlite
from pcapi import logtool

#################### Dropbox,flickr etc. credential storage management #############
"""  Wrapper functions around SQL command use for reading/writing/seaching access
credentials for different providers.

The result is normal a list of tuples e.g. [(foo,bar)] for one row and (None,) for no rows.

NOTE: req_key (in dropbox lingo) is "userid" for pcapi
"""

log = logtool.getLogger("tokens", "pcapi")

def dump_tokens():
    c = conn.cursor()
    res = c.execute("""
        SELECT * FROM tokens;
    """)
    # 2D list of lists
    return c.fetchall()

def save_access_tokens(userid, req_secret, acc_key, acc_secret):
    c = conn.cursor()
    c.execute(SAVE_ACCESS_TOKENS, (userid, req_secret, acc_key, acc_secret, userid))
    conn.commit()
    return c.rowcount == 1

def get_access_pair(userid):
    """ return ( acc_key, acc_secret ) for provided userid or None """
    c = conn.cursor()
    c.execute(GET_ACCESS_PAIR, (userid,))
    return c.fetchone()

def delete_token(userid):
    """ delete token with provided userid """
    c = conn.cursor()
    c.execute(DELETE_TOKEN, (userid,))
    conn.commit()
    return c.rowcount == 1

### temporary values #####

def get_request_pair(userid):
    """ return ( userid, req_secret ) pair for provided userid or None """
    c = conn.cursor()
    c.execute(GET_REQUEST_PAIR, (userid,))
    return c.fetchone()

def save_unverified_request( userid, req_secret ):
    """ save unverified request keys """
    c = conn.cursor()
    res = c.execute(SAVE_UNVERIFIED_REQUEST, (userid, req_secret, userid))
    conn.commit()
    return True

def delete_unverified_request(userid):
    """ Delete an user temporary request returns always True """
    c = conn.cursor()
    res = c.execute(DELETE_UNVERIFIED_REQUEST, (userid,))
    conn.commit()
    return True

def prune_temp_request():
    """ delete temporary requests tables. Should be called at app startup """
    c = conn.cursor()
    res = c.execute("""
        DELETE FROM temp_request(userid,reqsec)
        """)
    conn.commit()
    return True



### SQL #####

# placeholders differ in postgres and sqlite
if use_sqlite:
    ph = '?'
else:
    ph = '%s'

# token table

SAVE_ACCESS_TOKENS = """
INSERT INTO tokens(userid,reqsec,accsec,acckey) SELECT {0},{0},{0},{0} WHERE NOT EXISTS (SELECT 1 FROM tokens WHERE userid = {0})
""".format(ph)

GET_ACCESS_PAIR = """
SELECT accsec, acckey from tokens WHERE userid={0}
""".format(ph)

DELETE_TOKEN = """
DELETE FROM tokens WHERE userid={0}
""".format(ph)

# temp_request table
SAVE_UNVERIFIED_REQUEST = """
INSERT INTO temp_request(userid, reqsec) SELECT {0},{0} WHERE NOT EXISTS (SELECT 1 FROM temp_request WHERE userid = {0})
""".format(ph)

GET_REQUEST_PAIR = """
SELECT userid, reqsec from temp_request WHERE userid={0}
""".format(ph)

DELETE_UNVERIFIED_REQUEST = """
DELETE FROM temp_request WHERE userid={0}
""".format(ph)
