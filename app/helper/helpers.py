from app.db.db_connection import db_connection

def check_author(author_id):
    con = db_connection()
    cur = con.cursor()

    cur.execute(
        """
            SELECT EXISTS(SELECT 1 FROM authors WHERE author_id = %s);
        """, (author_id,)
    )

    res = cur.fetchone()
    cur.close()
    con.close()
    return bool(res[0])

def check_admin(admin_code):
    con = db_connection()
    cur = con.cursor()

    cur.execute(
        """
            SELECT EXISTS(SELECT 1 FROM admins WHERE admin_code = %s);
        """, (admin_code,)
    )

    res = cur.fetchone()
    cur.close()
    con.close()
    return bool(res[0])