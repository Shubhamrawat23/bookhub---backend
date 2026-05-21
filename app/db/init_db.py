from db_connection import db_connection

def create_tables():
    con = db_connection()
    cur = con.cursor()

    if not con:
        print("Database connection failed")
        return
    
    # Author table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS authors (
            author_id VARCHAR(20) PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100),
            password varchar(225) default null,
            phone VARCHAR(20),
            city VARCHAR(50),
            joined_date DATE
        );
    """)

    # Author's book table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS books (
            book_id VARCHAR(20) PRIMARY KEY,
            author_id VARCHAR(20),
            title VARCHAR(200),
            isbn VARCHAR(50),
            genre VARCHAR(100),
            publication_date DATE default null,
            status VARCHAR(100),
            mrp INTEGER DEFAULT NULL,
            author_royalty_per_copy INTEGER DEFAULT NULL,
            total_copies_sold INTEGER,
            total_royalty_earned INTEGER,
            royalty_paid INTEGER,
            royalty_pending INTEGER,
            last_royalty_payout_date DATE DEFAULT NULL,
            print_partner VARCHAR(100) DEFAULT NULL,
            available_on JSONB,
            FOREIGN KEY (author_id) REFERENCES authors(author_id)
        );
    """)

    # Admin table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            admin_id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100) UNIQUE,
            password VARCHAR(255),
            phone VARCHAR(20),
            created_at TIMESTAMPTZ DEFAULT NOW(),
            updated_at TIMESTAMPTZ DEFAULT NULL
        );
    """)

    # Author's query tkts table
    cur.execute("CREATE TYPE category_type AS ENUM ('General Level', 'Account Level');")
    cur.execute("""        
        CREATE TABLE IF NOT EXISTS query_tickets (
            id SERIAL PRIMARY KEY,
            ticket_code VARCHAR(30) UNIQUE,
            author_id VARCHAR(20),
            book_id VARCHAR(20) DEFAULT NULL,

            subject VARCHAR(255),
            description TEXT,

            attachment_url TEXT DEFAULT NULL,
            
            -- CATEGORY (General Level, Account Level)
            category category_type DEFAULT 'General Level',

            -- STATUS (0=open, 1=in_progress, 2=Resolved, 3=closed)
            status SMALLINT DEFAULT 0 
            /* 
                0 = Open
                1 = In Progress
                2 = Resolved
                3 = Closed
                4 = Re Open
            */,

            -- PRIORITY (1=Critical, 2=High, 3=Medium, 4=Low)
            priority SMALLINT DEFAULT 3
            /*
                1 = Critical
                2 = High
                3 = Medium
                4 = Low
            */,

            notes TEXT DEFAULT NULL,

            assigned_to INTEGER DEFAULT NULL,
            assigned_by INTEGER DEFAULT NULL,

            created_at TIMESTAMPTZ DEFAULT NOW(),
            updated_at TIMESTAMPTZ DEFAULT NOW(),

            FOREIGN KEY (author_id) REFERENCES authors(author_id),
            FOREIGN KEY (book_id) REFERENCES books(book_id),
            FOREIGN KEY (assigned_to) REFERENCES admins(admin_id),
            FOREIGN KEY (assigned_by) REFERENCES admins(admin_id)
        );
    """)

    # Tkt message history table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ticket_messages (
            id SERIAL PRIMARY KEY,
            ticket_code VARCHAR(30),
            sender_type VARCHAR(20),
            sender_id VARCHAR(50),
            message TEXT,
            created_at TIMESTAMPTZ DEFAULT NOW(),

            FOREIGN KEY (ticket_code) REFERENCES query_tickets(ticket_code)
        );
    """)
    con.commit()
    cur.close()
    con.close()
    print('All tables are created.')


if __name__ == "__main__":
    create_tables()