"""Oracle HR Demo Agent

A simple script that demonstrates how to connect to an Oracle database, run a query and a PL/SQL
procedure, and log the results. The script expects a ``credentials.json`` file in the project
root or a ``demo_agent/credentials.json`` path.

Requirements
------------
- Python 3.9+
- ``oracledb`` installed (``pip install oracledb``)
- No Oracle Instant Client is needed when using the default Thin mode.

Example ``credentials.json`` structure (the values are placeholders - replace them with real
credentials before running)::

    {
      "oracle": {
      "url": "host:1521/service",
        "user": "db_user",
        "pass": "db_password"
      }
    }

Running the script::

    python demo_agent/demo_agent.py

The script will:

1. Connect to Oracle using the ``oracle`` section in ``credentials.json``.
2. Retrieve and print employees whose ``department_id`` is 60.
3. Call ``inc_salary`` to increase salaries by 10 % for that department.
4. Print the output of ``INCREMENT$PROC``.
"""

import json
import re
import sys

import oracledb

# ---------------------------------------------------------------------------
# Configuration helpers
# ---------------------------------------------------------------------------

def load_credentials(path: str = "credentials.json") -> dict:
    """Load JSON credentials from the given file.

    The JSON is expected to contain an ``oracle`` key with ``url``, ``user`` and
    ``pass`` sub‑keys.
    """
    try:
        with open(path, "r", encoding="utf-8") as fp:
            data = json.load(fp)
    except FileNotFoundError:
        print(f"Credentials file '{path}' not found.", file=sys.stderr)
        sys.exit(1)
    if "oracle" not in data:
        print("Credentials file missing 'oracle' section.", file=sys.stderr)
        sys.exit(1)
    return data["oracle"]

# ---------------------------------------------------------------------------
# Oracle helpers
# ---------------------------------------------------------------------------

def connect_oracle(cfg: dict) -> oracledb.Connection:
    """Create a new Oracle database connection.

    ``cfg`` must contain the Oracle DSN (``host:port/service``), ``user`` and ``pass`` keys.
    """
    dsn = str(cfg.get("url", "")).strip()
    user = cfg["user"]
    pwd = cfg["pass"]
    if not dsn or not user or not pwd:
        print("Oracle configuration is incomplete: set url, user and pass in credentials.json.", file=sys.stderr)
        sys.exit(1)

    if re.search(r"\b(host|service|db-host\.example\.com|service-name)\b", dsn, re.IGNORECASE):
        print(
            "Oracle DSN still contains a sample value. Edit credentials.json and set url to "
            "the real database address, for example 'localhost:1521/XEPDB1' or '10.0.0.12:1521/ORCLPDB1'.",
            file=sys.stderr,
        )
        sys.exit(1)

    # python-oracledb defaults to Thin mode, which does not require Oracle Instant Client.
    try:
        return oracledb.connect(user=user, password=pwd, dsn=dsn)
    except oracledb.OperationalError as exc:
        message = str(exc)
        if "getaddrinfo failed" in message or "Errno 11001" in message:
            print(
                f"Cannot resolve Oracle host from DSN '{dsn}'. Check the host name and confirm "
                "the computer is connected to the required network or VPN.",
                file=sys.stderr,
            )
        else:
            print(f"Could not connect to Oracle using DSN '{dsn}': {message}", file=sys.stderr)
        sys.exit(1)

# ---------------------------------------------------------------------------
# Demo logic
# ---------------------------------------------------------------------------

DEPARTMENT_ID = 60

def get_employees_by_dept(cur: oracledb.Cursor, dept_id: int) -> None:
    """Retrieve employees for a department via stored procedure."""
    out_cursor = cur.var(oracledb.CURSOR)
    cur.callproc("HR.GET_EMPLOYEES_BY_DEPT", [dept_id, out_cursor])
    rows = out_cursor.getvalue()
    if not rows:
        print(f"No employees found for department {dept_id}.")
        return
    print(f"Employees in department {dept_id}:")
    for row in rows:
        emp_id, first_name, salary = row
        print(f"  {emp_id:<5} {first_name:<20} {salary:>10,.2f}")


def call_inc_salary(cur: oracledb.Cursor, dept_id: int) -> None:
    """Call the PL/SQL procedure ``inc_salary``.

    The procedure is expected to be defined in the HR schema and should
    accept a single IN parameter :p_dept.
    """
    try:
        cur.callproc("inc_salary", [dept_id])
        print(f"Procedure inc_salary called for department {dept_id}.")
    except oracledb.DatabaseError as exc:
        err, = exc.args
        print(f"Failed to execute inc_salary: {err.message}", file=sys.stderr)
        sys.exit(1)


# ---------------------------------------------------------------------------
# CRUD helpers
# ---------------------------------------------------------------------------


def init_db(cur: oracledb.Cursor) -> None:
    """Create HR.EMPLOYEES table, INC_SALARY procedure and insert sample data.
    If objects already exist, the errors are suppressed."""
    # Table
    try:
        cur.execute(
            """
            CREATE TABLE HR.EMPLOYEES (
                employee_id   NUMBER(6)   PRIMARY KEY,
                first_name    VARCHAR2(20) NOT NULL,
                last_name     VARCHAR2(25) NOT NULL,
                salary        NUMBER(10,2) NOT NULL,
                department_id NUMBER(4)    NOT NULL
            )
            """
        )
        cur.connection.commit()
    except oracledb.DatabaseError as exc:
        if exc.args[0].code != 955:  # ORA-00955: name exists
            raise
    # Procedure
    try:
        cur.execute(
            """
            CREATE OR REPLACE PROCEDURE HR.INC_SALARY(p_dept IN NUMBER) IS
            BEGIN
                UPDATE HR.EMPLOYEES
                SET salary = salary * 1.10
                WHERE department_id = p_dept;
                DBMS_OUTPUT.PUT_LINE('Salaries updated for dept ' || p_dept);
            END;
            """
        )
        cur.connection.commit()
    except oracledb.DatabaseError as exc:
        if exc.args[0].code != 955:
            raise
    # Sample data
    try:
        cur.execute("DELETE FROM HR.EMPLOYEES")  # clear old data
        cur.execute(
            """
            INSERT INTO HR.EMPLOYEES (employee_id, first_name, last_name, salary, department_id)
            VALUES (1001, 'JOHNS', 'DOE', 50000, 60),
                   (1002, 'JANE',  'RIPPLE', 60000, 60)
            """
        )
        cur.connection.commit()
    except oracledb.DatabaseError as exc:
        if exc.args[0].code != 4218:  # ORA-04218: object does not exist
            raise


def insert_employee(cur: oracledb.Cursor, employee_id: int, first_name: str, last_name: str, salary: float, department_id: int) -> None:
    """Insert a new employee into HR.EMPLOYEES."""
    cur.execute(
        "INSERT INTO HR.EMPLOYEES (employee_id, first_name, last_name, salary, department_id) VALUES (:1, :2, :3, :4, :5)",
        (employee_id, first_name, last_name, salary, department_id))
    cur.connection.commit()


def delete_employee(cur: oracledb.Cursor, employee_id: int) -> None:
    """Delete an employee by employee_id."""
    cur.execute("DELETE FROM HR.EMPLOYEES WHERE employee_id = :id", (employee_id,))
    cur.connection.commit()


def main():
    cfg = load_credentials()
    conn = connect_oracle(cfg)
    try:
        with conn.cursor() as cur:
            # Enable DBMS_OUTPUT for any future outputs
            cur.callproc("dbms_output.enable", [100000])
            try:
                get_employees_by_dept(cur, DEPARTMENT_ID)
            except RuntimeError as exc:
                print(f"Errore database: {exc}", file=sys.stderr)
                sys.exit(1)
            call_inc_salary(cur, DEPARTMENT_ID)
            # Show updated salaries
            get_employees_by_dept(cur, DEPARTMENT_ID)
            # Flush any DBMS_OUTPUT lines
            while True:
                try:
                    cur.execute("SELECT DBMS_OUTPUT.GET_LINE(output) FROM dual")
                    row = cur.fetchone()
                    if row is None or row[0] is None:
                        break
                    print("DBMS_OUTPUT:", row[0])
                except oracledb.DatabaseError:
                    break
    finally:
        conn.close()

if __name__ == "__main__":
    main()
