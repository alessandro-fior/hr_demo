# Demo Agent Documentation

## Purpose
The **demo agent** illustrates how to interact with an Oracle database using a simple *SQL → PL/SQL* workflow. It demonstrates:

1. **Connection** to the database (Oracle, PostgreSQL, SQL Server).
2. Executing a **SELECT** query.
3. Running a **PL/SQL procedure** that updates data.
4. Handling **exceptions**.

The agent is intentionally lightweight – no external dependencies beyond a JDBC/ODBC driver and the database.

## Configuration
Create a file named `credentials.json` in the same directory with the following structure (replace placeholders with actual values):

```json
{
  "oracle": {
    "url": "jdbc:oracle:thin:@//host:1521/service",
    "user": "db_user",
    "pass": "db_password"
  },
  "postgres": {
    "url": "jdbc:postgresql://host:5432/dbname",
    "user": "pg_user",
    "pass": "pg_password"
  },
  "sqlserver": {
    "url": "jdbc:sqlserver://host:1433;databaseName=dbname",
    "user": "sql_user",
    "pass": "sql_password"
  }
}
```

> **Note**: The demo agent reads this file at startup and uses the `oracle` section by default.

## Usage
Run the agent script (e.g., `demo_agent.py`). The agent will:

1. Connect to Oracle.
2. Retrieve and display employees from department 60.
3. Execute the `inc_salary` procedure.
4. Display the result of the salary increase.

```bash
python demo_agent.py
```

## Extending the Agent
Feel free to add new PL/SQL blocks or change the target department. The core logic lives in `demo_agent.py` to keep the example focused on the database interaction rather than framework plumbing.

---

**Tip**: If you don't have a local Oracle instance, consider using Oracle XE or a Docker image.

---

**Contributors**: Inspired by the `hr.txt` sample.
