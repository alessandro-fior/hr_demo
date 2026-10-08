-- 00_dml – Creazione utenti, grant e tabella HR.EMPLOYEES
-- 
-- Esegui prima di avviare l’agent.
-- 
-- 1.  Utente HR (schema base)
CREATE USER HR IDENTIFIED BY <hr_password>;
GRANT CONNECT, RESOURCE, UNLIMITED TABLESPACE TO HR;

-- 2.  Utente CLIENTE (auto‑uso dell’agent)
CREATE USER CLIENTE IDENTIFIED BY <cliente_password>;
GRANT CONNECT, RESOURCE, UNLIMITED TABLESPACE TO CLIENTE;

-- 3.  Grandi privilegi per l’utente CLIENTE
GRANT SELECT, UPDATE ON HR.EMPLOYEES TO CLIENTE;
GRANT EXECUTE ON HR.INC_SALARY TO CLIENTE;

-- 4.  Tabella di esempio
CREATE TABLE HR.EMPLOYEES (
    employee_id   NUMBER(6) PRIMARY KEY,
    first_name    VARCHAR2(20) NOT NULL,
    last_name     VARCHAR2(25) NOT NULL,
    salary        NUMBER(10,2) NOT NULL,
    department_id NUMBER(4) NOT NULL
);
