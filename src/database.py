"""Module for executing database queries."""

import psycopg2


def postgresql_query(psql_config, query_params, commit=False):
    """Executes the PostgreSQL database query and returns the results and any
    database errors as a list of strings."""
    conn = None
    results = None
    errors = list()

    try:
        conn = psycopg2.connect(**psql_config)
        cur = conn.cursor()

        cur.execute(*query_params)
        results = cur.fetchall()

        if commit:
            conn.commit()

        cur.close()

    except psycopg2.DatabaseError as err:
        errors.append(str(err))

    finally:
        if conn is not None:
            conn.close()

    return results, errors
