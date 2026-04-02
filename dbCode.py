# dbCode.py
# Author: Kaitlyn Staut
# Helper functions for database connection and queries

import pymysql
import creds
import uuid
import boto3

def get_conn():
    """Returns a connection to the MySQL RDS instance."""
    conn = pymysql.connect(
        host=creds.host,
        user=creds.user,
        password=creds.password,
        db=creds.db,
    )
    return conn

def execute_query(query, args=()):
    """Executes a SELECT query and returns all rows as dictionaries."""
    conn = get_conn()
    cur = get_conn().cursor(pymysql.cursors.DictCursor)
    cur.execute(query, args)
    conn.commit()
    rows = cur.fetchall()
    cur.close()
    return rows

# Used AI to come up with this:
def execute_insert(query, args=()):
    conn = get_conn()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute(query, args)
    conn.commit()
    last_id = cur.lastrowid # gets the ID of the row that was just inserted.
    cur.close()
    return last_id
