# Schema and Table Creation Instructions for CLIENTE

## Purpose
These steps guide a DBA in setting up the **CLIENTE** schema, the **HR** schema (if it does not already exist), and the **EMPLOYEES** table so the demo agent can access data and execute the `INC_SALARY` procedure.

---

## 1. Check for existing HR schema

```sql
SELECT username
FROM   dba_users
WHERE  username = 'HR';
```

* **If a row is returned**, the HR schema already exists – skip to section 2.
* **If no rows are returned**, you must create the HR schema and populate it with the sample data.

## 2. Create HR schema (optional)

```sql
-- Connect as a privileged user (e.g., SYS)
CREATE USER HR IDENTIFIED BY <hr_password>;
GRANT CONNECT, RESOURCE TO HR;

-- Create the EMPLOYEES table within HR
CREATE TABLE HR.EMPLOYEES (
    employee_id   NUMBER(6)   PRIMARY KEY,
    first_name    VARCHAR2(20) NOT NULL,
    last_name     VARCHAR2(25) NOT NULL,
    salary        NUMBER(10,2) NOT NULL,
    department_id NUMBER(4)    NOT NULL
);

-- Insert sample data
INSERT INTO HR.EMPLOYEES VALUES (1001, 'JOHNS', 'DOE', 50000, 60);
INSERT INTO HR.EMPLOYEES VALUES (1002, 'JANE',  'RIPPLE', 60000, 60);
COMMIT;

-- (Optional) Create the INC_SALARY procedure
CREATE OR REPLACE PROCEDURE HR.INC_SALARY(p_dept IN NUMBER) IS
BEGIN
    UPDATE HR.EMPLOYEES
    SET salary = salary * 1.10
    WHERE department_id = p_dept;
    DBMS_OUTPUT.PUT_LINE('Salaries updated for dept ' || p_dept);
END;
```

Replace `<hr_password>` with a secure password.

## 3. Create CLIENTE schema (if it does not exist)

```sql
CREATE USER CLIENTE IDENTIFIED BY <cliente_password>;
GRANT CONNECT, RESOURCE TO CLIENTE;
```

Replace `<cliente_password>` with a secure password.

## 4. Grant necessary privileges to CLIENTE

The demo agent requires

* **SELECT** on `HR.EMPLOYEES` (and **UPDATE** if the procedure modifies the table).
* **EXECUTE** on `HR.INC_SALARY`.

```sql
GRANT SELECT, UPDATE ON HR.EMPLOYEES TO CLIENTE;
GRANT EXECUTE ON HR.INC_SALARY TO CLIENTE;
```

> **Tip:** Verify the procedure exists:
> ```sql
> SELECT object_name, object_type
> FROM   dba_objects
> WHERE  owner = 'HR' AND object_type = 'PROCEDURE' AND object_name = 'INC_SALARY';
> ```

## 5. Verify access from CLIENTE

```sql
-- Connect as CLIENTE
CONNECT CLIENTE/<cliente_password>@<tns_alias>;

-- Test SELECT
SELECT * FROM HR.EMPLOYEES WHERE department_id = 60;

-- Test procedure call
BEGIN
    HR.INC_SALARY(60);
END;
```

If the `SELECT` and procedure call succeed, the demo agent will run without raising `ORA-00942`.

---

**Note**: The demo agent’s `print_employees` function does not qualify the table with `HR.`. It relies on the configured user having the appropriate privileges. If you prefer to use a fully qualified name, modify the query in `demo_agent.py` accordingly.
