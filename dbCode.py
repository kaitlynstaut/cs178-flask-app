# dbCode.py
# Author: Kaitlyn Staut
# Helper functions for database connection and queries

import pymysql
import boto3
import creds

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
