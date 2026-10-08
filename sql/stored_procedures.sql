-- HR schema initialization
-- Assumes HR and CLIENTE users exist and necessary privileges granted.

-- 1. Create the EMPLOYEES table
CREATE TABLE HR.EMPLOYEES (
    employee_id   NUMBER(6) PRIMARY KEY,
    first_name    VARCHAR2(20) NOT NULL,
    last_name     VARCHAR2(25) NOT NULL,
    salary        NUMBER(10,2) NOT NULL,
    department_id NUMBER(4) NOT NULL
);

-- 2. Stored procedures
-- 2.1 Get employees by department (returns refcursor)
CREATE OR REPLACE PROCEDURE HR.GET_EMPLOYEES_BY_DEPT(
    p_dept IN NUMBER,
    p_cursor OUT SYS_REFCURSOR
) AS
BEGIN
    OPEN p_cursor FOR
        SELECT employee_id, first_name, salary
        FROM HR.EMPLOYEES
        WHERE department_id = p_dept;
END;
/

-- 2.2 Increment salaries for a department
CREATE OR REPLACE PROCEDURE HR.INC_SALARY(p_dept IN NUMBER) AS
BEGIN
    UPDATE HR.EMPLOYEES
    SET salary = salary * 1.10
    WHERE department_id = p_dept;
    DBMS_OUTPUT.PUT_LINE('Salaries updated for dept ' || p_dept);
END;
/
-- 2.3 Insert a new employee
CREATE OR REPLACE PROCEDURE HR.INSERT_EMPLOYEE(
    p_employee_id IN NUMBER,
    p_first_name IN VARCHAR2,
    p_last_name IN VARCHAR2,
    p_salary IN NUMBER,
    p_department_id IN NUMBER
) AS
BEGIN
    INSERT INTO HR.EMPLOYEES (employee_id, first_name, last_name, salary, department_id)
    VALUES (p_employee_id, p_first_name, p_last_name, p_salary, p_department_id);
    COMMIT;
END;
/
-- 2.4 Delete an employee
CREATE OR REPLACE PROCEDURE HR.DELETE_EMPLOYEE(p_employee_id IN NUMBER) AS
BEGIN
    DELETE FROM HR.EMPLOYEES WHERE employee_id = p_employee_id;
    COMMIT;
END;
/
-- 3. Sample data
INSERT INTO HR.EMPLOYEES VALUES (1001, 'JOHNS', 'DOE', 50000, 60);
INSERT INTO HR.EMPLOYEES VALUES (1002, 'JANE',  'RIPPLE', 60000, 60);
COMMIT;
