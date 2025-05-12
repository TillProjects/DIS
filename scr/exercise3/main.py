import argparse
from typing import Tuple

import psycopg2
import os
from dotenv import load_dotenv
from psycopg2.extensions import ISOLATION_LEVEL_READ_COMMITTED, ISOLATION_LEVEL_SERIALIZABLE, connection, cursor

load_dotenv()

dis_db_password = os.getenv("REMOTE_POSTGRES_DIS_PASSWORD")

conn_params = {
    'host': 'vsisdb.informatik.uni-hamburg.de',
    'dbname': 'dis-2025',
    'user': 'vsisp42',
    'password': dis_db_password
}

def reset_table():
    with psycopg2.connect(**conn_params) as conn:
        with conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS sheet3;")
            cur.execute("""
                CREATE TABLE sheet3 (
                    id SERIAL PRIMARY KEY,
                    name TEXT
                );
            """)
            cur.execute("INSERT INTO sheet3 (name) VALUES ('Till'), ('Victor'), ('Anna');")
        conn.commit()

def get_connection_and_cursor(
    tx_name: str = "",
    isolation_level: int = ISOLATION_LEVEL_READ_COMMITTED,
    print_isolation: bool = False,
) -> Tuple[connection, cursor]:
    conn = psycopg2.connect(**conn_params)
    conn.set_session(isolation_level=isolation_level, autocommit=False)
    cur = conn.cursor()

    if print_isolation:
        cur.execute("SHOW TRANSACTION ISOLATION LEVEL;")
        level = cur.fetchone()[0]
        label = f" [{tx_name}]" if tx_name else ""
        print(f"Isolation level{label}: {level}")

    return conn, cur


def run_schedule_S1(isolation_level: int = ISOLATION_LEVEL_READ_COMMITTED):
    print("\n=== Running S1 ===")

    conn1, cur1 = get_connection_and_cursor("T1", isolation_level, True)
    conn2, cur2 = get_connection_and_cursor("T2", isolation_level, True)

    print('S1 = r1(x) w2(x) c2 w1(x) r1(x) c1')

    # r1(x)
    cur1.execute("SELECT name FROM sheet3 WHERE id = 1;")
    print(f"r1(x): {cur1.fetchone()[0]}")

    # w2(x)
    cur2.execute("UPDATE sheet3 SET name = 'from T2' WHERE id = 1;")
    print(f"w2(x)")

    # c2
    conn2.commit()
    print("T2 committed")

    # w1(x)
    cur1.execute("UPDATE sheet3 SET name = 'from T1' WHERE id = 1;")
    print(f"w1(x)")

    # r1(x)
    cur1.execute("SELECT name FROM sheet3 WHERE id = 1;")
    print(f"r1(x): {cur1.fetchone()[0]}")

    # c1
    conn1.commit()
    print("T1 committed")

    cur1.close()
    conn1.close()
    cur2.close()
    conn2.close()

    with psycopg2.connect(**conn_params) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT name FROM sheet3 WHERE id = 1;")
            print(f"[S1 Result] Final value of x (name): {cur.fetchone()[0]}")

def run_schedule_S2(isolation_level: int = ISOLATION_LEVEL_READ_COMMITTED):
    print("\n=== Running S2 ===")

    conn1, cur1 = get_connection_and_cursor(isolation_level=isolation_level)
    conn2, cur2 = get_connection_and_cursor(isolation_level=isolation_level)

    print('S2 = r1(x) w2(x) c2 r1(x) c1')

    # r1(x)
    cur1.execute("SELECT name FROM sheet3 WHERE id = 1;")
    print(f"r1(x): {cur1.fetchone()[0]}")

    # w2(x)
    cur2.execute("UPDATE sheet3 SET name = 'from T2' WHERE id = 1;")
    print("w2(x)")

    # c2
    conn2.commit()
    print("T2 committed")

    # r1(x)
    cur1.execute("SELECT name FROM sheet3 WHERE id = 1;")
    print(f"r1(x): {cur1.fetchone()[0]}")

    # c1
    conn1.commit()
    print("T1 committed")

    cur1.close()
    conn1.close()
    cur2.close()
    conn2.close()

    with psycopg2.connect(**conn_params) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT name FROM sheet3 WHERE id = 1;")
            print(f"[S2 Result] Final value of x (name): {cur.fetchone()[0]}")


def run_schedule_S3(isolation_level: int = ISOLATION_LEVEL_READ_COMMITTED):
    print("\n=== Running S3 ===")

    conn1, cur1 = get_connection_and_cursor(isolation_level=isolation_level)
    conn2, cur2 = get_connection_and_cursor(isolation_level=isolation_level)

    print('S3 = r2(x) w1(x) w1(y) c1 r2(y) w2(x) w2(y) c2')

    # r2(x)
    cur2.execute("SELECT name FROM sheet3 WHERE id = 1;")
    print(f"r2(x): {cur2.fetchone()[0]}")

    # w1(x)
    cur1.execute("UPDATE sheet3 SET name = 'from T1-x' WHERE id = 1;")
    print("w1(x)")

    # w1(y)
    cur1.execute("UPDATE sheet3 SET name = 'from T1-y' WHERE id = 2;")
    print("w1(y)")

    # c1
    conn1.commit()
    print("T1 committed")

    # r2(y)
    cur2.execute("SELECT name FROM sheet3 WHERE id = 2;")
    print(f"r2(y): {cur2.fetchone()[0]}")

    # w2(x)
    cur2.execute("UPDATE sheet3 SET name = 'from T2-x' WHERE id = 1;")
    print("w2(x)")

    # w2(y)
    cur2.execute("UPDATE sheet3 SET name = 'from T2-y' WHERE id = 2;")
    print("w2(y)")

    # c2
    conn2.commit()
    print("T2 committed")

    cur1.close()
    conn1.close()
    cur2.close()
    conn2.close()

    with psycopg2.connect(**conn_params) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name FROM sheet3 WHERE id IN (1, 2) ORDER BY id;")
            results = cur.fetchall()
            print(f"[S3 Result] Final values:")
            for row in results:
                print(f"  id={row[0]}, name={row[1]}")


def run_schedule_with_error_handling(schedule_func, isolation_level: int = ISOLATION_LEVEL_READ_COMMITTED):
    try:
        schedule_func(isolation_level)
    except psycopg2.Error as e:
        print(f"Error occurred: {e}")
        if isinstance(e, psycopg2.errors.SerializationFailure):
            print(
                "Serialization failure: Transaction could not be completed due to concurrent update."
            )
        else:
            print("An unexpected error occurred during the transaction.")


def main():
    parser = argparse.ArgumentParser(description="Run transaction schedules with specified isolation level.")
    parser.add_argument('isolation', choices=['rc', 'sr'], help="Choose the isolation level: 'rc' for Read Committed or 'sr' for Serializable")

    args = parser.parse_args()
    isolation_level = None

    if args.isolation == 'rc':
        isolation_level = ISOLATION_LEVEL_READ_COMMITTED
        print("\n=== Running with isolation level READ COMMITTED ===")
    elif args.isolation == 'sr':
        isolation_level = ISOLATION_LEVEL_SERIALIZABLE
        print("\n=== Running with isolation level SERIALIZABLE ===")

    if isolation_level is None:
        print("Error: Isolation level was not correctly set.")
        return

    reset_table()
    run_schedule_with_error_handling(run_schedule_S1, isolation_level)

    reset_table()
    run_schedule_with_error_handling(run_schedule_S2, isolation_level)

    reset_table()
    run_schedule_with_error_handling(run_schedule_S3, isolation_level)

if __name__ == '__main__':
    main()
