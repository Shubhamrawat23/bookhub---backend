from db_connection import db_connection
import json
import hashlib

def seed_database():
    # Set admin password manually
    admin_hash_password = hashlib.sha256("admin@123".encode()).hexdigest()

    con = db_connection()

    if not con:
        print("Database connection failed")
        return
    
    cur = con.cursor()

    with open('app/db/data.json', 'r', encoding='Utf-8') as file:
        data = json.load(file)
    
    # Insert data of author
    for author in data["authors"]:
        cur.execute("""
            INSERT INTO authors (
                author_id,
                name,
                email,
                phone,
                city,
                joined_date
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (author_id) DO NOTHING;
        """, (
            author["author_id"],
            author["name"],
            author["email"],
            author["phone"],
            author["city"],
            author["joined_date"]
        ))

        # Insert data of author' book
        for book in author["books"]:
            cur.execute("""
                INSERT INTO books (
                    book_id,
                    author_id,
                    title,
                    isbn,
                    genre,
                    publication_date,
                    status,
                    mrp,
                    author_royalty_per_copy,
                    total_copies_sold,
                    total_royalty_earned,
                    royalty_paid,
                    royalty_pending,
                    last_royalty_payout_date,
                    print_partner,
                    available_on
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (book_id) DO NOTHING;
            """, (
                book["book_id"],
                author["author_id"],
                book["title"],
                book["isbn"],
                book["genre"],
                book["publication_date"],
                book["status"],
                book["mrp"],
                book["author_royalty_per_copy"],
                book["total_copies_sold"],
                book["total_royalty_earned"],
                book["royalty_paid"],
                book["royalty_pending"],
                book["last_royalty_payout_date"],
                book["print_partner"],
                json.dumps(book["available_on"])
            ))

    # Insert Data in Admin Table
    cur.execute(
        """
        INSERT INTO admins (
            name,
            email,
            password
        )
        VALUES(%s, %s, %s)
        ON CONFLICT (admin_id) DO NOTHING;
        """,(
            "ADMIN_00001",
            "admin_00001@bookleafpub.com",
            admin_hash_password
        )
    )

    
    con.commit()
    cur.close()
    con.close()

    print("Data added")


if __name__ == "__main__":
    seed_database()