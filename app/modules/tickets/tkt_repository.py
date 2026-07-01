from app.db.db_connection import db_connection
from psycopg2.extras import RealDictCursor

# Create entery in table query_tickets
def entry_in_query_tkts(ticket_code, author_id, book_id, subject, description, category="General Level", attachment_url="", status = 0, priority=3):
    con = db_connection()
    cur = con.cursor()
    
    cur.execute(
        """
        INSERT INTO query_tickets (
            ticket_code,
            author_id,
            book_id,
            subject,
            description,
            category,
            attachment_url,
            status,
            priority
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING ticket_code;
        """,(
            ticket_code,
            author_id,
            book_id,
            subject,
            description,
            category,
            attachment_url,
            status,
            priority
        )
    )
    data = cur.fetchone()
    con.commit()
    cur.close()
    con.close()

    return data


# Check that author created prev tkt or not
def check_tkt_existed(author_id=""):
    con = db_connection()
    cur = con.cursor()

    cur.execute("SELECT COUNT(id) FROM query_tickets WHERE author_id = %s;",(author_id,))
    data= cur.fetchone()
    cur.close()
    con.close()
    return data[0]


# Start convo with against new id
def save_converstion(ticket_code, sender_id, sender_type = "", message=""):
    con = db_connection()
    cur = con.cursor()

    cur.execute(
        """
            INSERT INTO ticket_messages (
                ticket_code,
                sender_id,
                sender_type,
                message
            ) VALUES(%s, %s, %s, %s) RETURNING id;
        """,(
            ticket_code,
            sender_id,
            sender_type,
            message
        )
    )
    data = cur.fetchone()
    con.commit()
    cur.close()
    con.close()

    return data[0]


# fetch all tkts list
def fetch_authors_tkt(author_id, role, status_filter="", category_filter="", priority_filter="", start_date_tz="", end_date_tz=""):
    con = db_connection()
    cur = con.cursor(cursor_factory=RealDictCursor)

    filters = []
    filter_val = []

    if (role.lower() == "admin"):
        if status_filter != "":
            filters.append('t.status = %s')
            filter_val.append(status_filter)

        if category_filter != "":
            filters.append('t.category = %s')
            filter_val.append(category_filter)

        if priority_filter != "":
            filters.append('t.priority = %s')
            filter_val.append(priority_filter)

        if start_date_tz != "":
            filters.append('t.created_at >= %s')
            filter_val.append(start_date_tz)

        if end_date_tz != "":
            filters.append('t.created_at < %s')
            filter_val.append(end_date_tz)

        filters_where = f"WHERE {' AND '.join(filters)}" if filters else ""

        cur.execute(f"SELECT t.*, a.name FROM query_tickets t LEFT JOIN authors a ON a.author_id = t.author_id {filters_where} ORDER BY id DESC;", tuple(filter_val))
    if(role.lower() == "author"):
        cur.execute(
            """
                SELECT id, ticket_code, subject, description, category, status, priority, attachment_url, created_at FROM query_tickets WHERE author_id = %s ORDER BY id DESC;
            """,(author_id,)
        )

    rows = cur.fetchall()

    cur.close()
    con.close()
    return rows


#  chat history
def get_chat_history(ticket_code, access_by=""):
    con = db_connection()
    cur = con.cursor(cursor_factory=RealDictCursor)

    if not access_by or access_by.strip() == "" or (access_by.lower() != "author" and access_by.lower() != "admin"):
        return None
    
    cur.execute(
        """
            SELECT * from ticket_messages WHERE ticket_code = %s ORDER BY id ASC;
        """, (ticket_code,)
    )

    data = cur.fetchall()
    cur.close()
    con.close()

    return data

# send chat against tkt
def save_chat(ticket_code, sender_id, sender_type="", message=""):
    con = db_connection()
    cur = con.cursor()

    cur.execute(
        """
            INSERT INTO ticket_messages (
            ticket_code,
            sender_id,
            sender_type,
            message
            ) VALUES (%s, %s, %s, %s) RETURNING id;
        """, (ticket_code, sender_id, sender_type, message)
    )
    id = cur.fetchone()
    con.commit()

    cur.close()
    con.close()

    return id
    

# Update the action for admin
# status (0=open, 1=in_progress, 2=Resolved, 3=closed)
# priority (1=Critical, 2=High, 3=Medium, 4=Low)

def save_action_for_tkt(ticket_code, action=None, action_val=None):
    con = db_connection()
    cur = con.cursor()

    if action_val is not None and action is not None:
        cur.execute(f"UPDATE query_tickets SET {action} = %s WHERE ticket_code = %s RETURNING id;",(action_val, ticket_code))
        data = cur.fetchone()

        con.commit()
        cur.close()
        con.close()

        return data
    
    return None


def fetch_tkt_data_for_admin(ticket_code):
    con = db_connection()
    cur = con.cursor(cursor_factory=RealDictCursor)

    cur.execute(
        """
            SELECT qt.*, a.name as assigned_to FROM query_tickets qt LEFT JOIN admins a ON a.admin_id = qt.assigned_to WHERE ticket_code = %s;
        """,(ticket_code,)
    )

    data = cur.fetchone()
    cur.close()
    con.close()
    return data