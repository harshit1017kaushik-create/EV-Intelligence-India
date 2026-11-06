
import os
import mysql.connector
import pandas as pd
import streamlit as st


def get_db_config():
    """
    Read database credentials from Streamlit Secrets
    or environment variables.
    """
    if "mysql" in st.secrets:
        config = dict(st.secrets["mysql"])
    else:
        config = {
            "host": os.getenv("DB_HOST"),
            "port": int(os.getenv("DB_PORT", 3306)),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "database": os.getenv("DB_NAME", "ev_intelligence"),
            "ssl_ca": os.getenv("DB_SSL_CA")
        }

    required_fields = ["host", "user", "password", "database"]

    missing_fields = [
        field for field in required_fields
        if not config.get(field)
    ]

    if missing_fields:
        raise ValueError(
            "Missing database configuration: "
            + ", ".join(missing_fields)
        )

    return config


def get_connection():
    """
    Establish a secure connection to Aiven MySQL.
    """
    config = get_db_config()

    connection_config = {
        "host": config["host"],
        "port": int(config.get("port", 3306)),
        "user": config["user"],
        "password": config["password"],
        "database": config.get("database", "ev_intelligence"),
        "connection_timeout": 15
    }

    ssl_ca = config.get("ssl_ca")

    if ssl_ca:
        connection_config["ssl_ca"] = ssl_ca
        connection_config["ssl_verify_cert"] = True

    return mysql.connector.connect(**connection_config)


@st.cache_data(ttl=300, show_spinner=False)
def fetch_dataframe(query, params=None):
    """
    Execute a SELECT query and return a Pandas DataFrame.

    Results are cached for 5 minutes to reduce
    repeated database queries.
    """
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(query, params or ())
        records = cursor.fetchall()

        return pd.DataFrame(records)

    finally:
        cursor.close()
        connection.close()


def test_connection():
    """
    Test whether the database connection is working.
    """
    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()

        return result[0] == 1

    finally:
        cursor.close()
        connection.close()
