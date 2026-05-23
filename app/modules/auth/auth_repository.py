from app.db.db_connection import db_connection

def authorLogin(email: str):
    con = db_connection()
    cur = con.cursor()
    data = cur.execute("SELECT author_id, name, email, phone, password FROM authors WHERE email = %s;",(email,))
    data = cur.fetchone()
    cur.close()
    con.close()
    return data

def author_forgot_password(email: str, new_password: str):
    con = db_connection()
    cur = con.cursor()
    data = cur.execute("UPDATE authors SET password = %s WHERE email = %s RETURNING author_id;", (new_password, email))
    data = cur.fetchone()
    con.commit()
    cur.close()
    con.close()
    return data


def adminLogin(email: str):
    con = db_connection()
    cur = con.cursor()
    data = cur.execute("SELECT admin_id, admin_code, name, email, password FROM admins WHERE email = %s;",(email,))
    data = cur.fetchone()
    cur.close()
    con.close()
    return data