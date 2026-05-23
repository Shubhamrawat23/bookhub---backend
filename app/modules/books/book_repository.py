from app.db.db_connection import db_connection
from psycopg2.extras import RealDictCursor

def get_books(author_id):
    con = db_connection()
    cur = con.cursor(cursor_factory=RealDictCursor)

    cur.execute(
        """
            SELECT * FROM books WHERE author_id = %s;
        """,(author_id,)
    )

    data = cur.fetchall()

    cur.close()
    con.close()

    return data