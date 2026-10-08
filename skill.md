# CRUD Skill for Demo Agent

## Purpose
This skill extends the **demo agent** with **Create / Read / Delete** operations on the `HR.EMPLOYEES` table.  It demonstrates:

1.  **`init_db()`** – sets up the schema, creates the table, the `INC_SALARY` procedure, and inserts sample rows (if they do not exist).
2.  **`insert_employee()`** – inserts a new employee record.
3.  **`delete_employee()`** – removes an employee by `employee_id`.
4.  **`print_employees()`** – reads and prints all employees in a specified department.

The skill is intentionally simple, using pure Python and the `oracledb` driver, making it easy to understand and integrate into larger projects.

---

### Usage Example
```python
from demo_agent.demo_agent import init_db, insert_employee, delete_employee, print_employees

conn = demo_agent.connect_oracle(demo_agent.load_credentials())
with conn.cursor() as cur:
    init_db(cur)                            # Ensure tables exist
    insert_employee(cur, 1003, 'ALICE', 'SMITH', 55000, 60)  # New record
    print_employees(cur, 60)                 # Verify insertion
    delete_employee(cur, 1003)               # Clean up
    print_employees(cur, 60)
conn.close()
```
