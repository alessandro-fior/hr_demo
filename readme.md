# Oracle HR Demo

Questo progetto dimostra una semplice interazione con Oracle: una query SQL, la chiamata a una procedura PL/SQL e la gestione degli errori.

## Prerequisiti

- Python 3.9 o successivo (incluso Python 3.14).
- Un database Oracle con lo schema HR.
- Il driver Python `oracledb`, che in modalità Thin non richiede Oracle Instant Client.

## Configurazione

Copia il file di esempio e inserisci i dati di connessione reali:

```powershell
Copy-Item demo_agent/credentials.json.sample credentials.json
```

Nel campo `url` usa il DSN nel formato `host:1521/service`, ad esempio `localhost:1521/XEPDB1`. Il programma legge `credentials.json` dalla cartella principale.

## Installazione ed esecuzione

Dalla cartella principale del progetto:

```powershell
python -m pip install -r demo_agent/requirements.txt
python demo_agent/demo_agent.py
```

Il programma legge i dipendenti del reparto 60 e chiama `inc_salary` per aggiornare gli stipendi. Verifica che la procedura esista nello schema prima di eseguire il demo.

## Procedura di esempio

```sql
CREATE OR REPLACE PROCEDURE inc_salary(p_dept IN NUMBER) IS
BEGIN
  UPDATE employees
     SET salary = salary * 1.10
   WHERE department_id = p_dept;

  DBMS_OUTPUT.PUT_LINE(SQL%ROWCOUNT || ' rows updated');
  COMMIT;
EXCEPTION
  WHEN OTHERS THEN
    ROLLBACK;
    DBMS_OUTPUT.PUT_LINE('Error: ' || SQLERRM);
END;
/
```
