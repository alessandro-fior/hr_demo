# Demo Agent

## Description
The **Demo Agent** is a lightweight Python script that connects to an Oracle database, queries employees from a department and runs a PL/SQL procedure to increment salaries.  It serves as a minimal but complete example of:

- Connecting to Oracle with a JSON‑formatted credential file.
- Executing a **SELECT** and a **PL/SQL** procedure.
- Handling permissions and error reporting.
- Optionally performing CRUD operations via added helper functions.

---

## Main Components
| Module | Responsibility |
|--------|---------------|
| `demo_agent/demo_agent.py` | Core logic, database connection & main workflow |
| `sql/init_db.sql` | Optional SQL script to initialise the schema for fresh instances |
| `scripts/check_docker.sh` | Verify Docker is running |
| `scripts/list_oracle_ports.sh` | Identify exposed ports of Oracle containers |

## Running the Agent
```bash
# 1. Ensure Docker is running and the Oracle container is up
source scripts/check_docker.sh
source scripts/list_oracle_ports.sh

# 2. Point credentials.json to the correct DSN
#    e.g., {
#      "oracle": {"url": "localhost:1521/XEPDB1", "user": "CLIENTE", "pass": "mypassword"}
#    }

# 3. Execute the agent
python demo_agent/demo_agent.py
```

The agent will:

1. Connect to Oracle.
2. Print employees in department 60.
3. Call `INC_SALARY` to bump salaries by 10 %.
4. Print employees again so you can see the salary change.

> **Tip**: If you want to test the CRUD helpers, drop in the `init_db`, `insert_employee`, and `delete_employee` functions (they are already present in the module).  Use them in a separate script or by adding a small test block at the bottom of `demo_agent.py`.
