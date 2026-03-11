import logging
from data import get_connection


def validate_id(emp_id):
    return emp_id.isdigit()


def insert_employee(emp_id, name, dept):

    db = get_connection()
    if not db:
        return False, "Database connection failed"

    try:
        cursor = db.cursor()
        query = "INSERT INTO empDetails (empId, empName, empDept) VALUES (%s,%s,%s)"
        cursor.execute(query, (emp_id, name, dept))
        db.commit()

        logging.info(f"Inserted employee {emp_id}")

        return True, "Employee added"

    except Exception as e:
        logging.error(f"Insert error: {e}")
        return False, str(e)

    finally:
        db.close()


def update_employee(emp_id, name, dept):

    db = get_connection()
    if not db:
        return False, "Database connection failed"

    try:
        cursor = db.cursor()

        query = "UPDATE empDetails SET empName=%s, empDept=%s WHERE empId=%s"
        cursor.execute(query, (name, dept, emp_id))
        db.commit()

        if cursor.rowcount == 0:
            return False, "Employee not found"

        logging.info(f"Updated employee {emp_id}")
        return True, "Employee updated"

    except Exception as e:
        logging.error(f"Update error: {e}")
        return False, str(e)

    finally:
        db.close()


def get_employee(emp_id):

    db = get_connection()
    if not db:
        return None

    try:
        cursor = db.cursor()

        query = "SELECT empName, empDept FROM empDetails WHERE empId=%s"
        cursor.execute(query, (emp_id,))

        row = cursor.fetchone()

        return row

    except Exception as e:
        logging.error(f"Fetch error: {e}")
        return None

    finally:
        db.close()


def delete_employee(emp_id):

    db = get_connection()
    if not db:
        return False

    try:
        cursor = db.cursor()

        query = "DELETE FROM empDetails WHERE empId=%s"
        cursor.execute(query, (emp_id,))
        db.commit()

        logging.info(f"Deleted employee {emp_id}")

        return cursor.rowcount > 0

    except Exception as e:
        logging.error(f"Delete error: {e}")
        return False

    finally:
        db.close()


def get_all_employees():

    db = get_connection()
    if not db:
        return []

    try:
        cursor = db.cursor()

        cursor.execute("SELECT * FROM empDetails")

        return cursor.fetchall()

    except Exception as e:
        logging.error(f"Fetch all error: {e}")
        return []

    finally:
        db.close()