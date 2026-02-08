import sqlite3


def create_database():
    # Connect to (or create) the database file
    conn = sqlite3.connect("university.db")
    cursor = conn.cursor()

    # 1. Create the 'students' table
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS students
                   (
                       student_id
                       TEXT
                       PRIMARY
                       KEY,
                       name
                       TEXT,
                       gpa
                       REAL,
                       status
                       TEXT,
                       notes
                       TEXT
                   )
                   """)

    # 2. Insert Dummy Data (Accepted, Rejected, Pending cases)
    students_data = [
        ("STU-1001", "Alice Smith", 3.9, "ACCEPTED", "Presidential Scholarship Awarded."),
        ("STU-1002", "Bob Jones", 2.2, "REJECTED", "GPA below the 2.5 requirement."),
        ("STU-1003", "Charlie Brown", 3.5, "PENDING", "Waiting for final semester transcripts."),
        ("STU-1004", "Diana Prince", 4.0, "ACCEPTED", "Direct admission to Computer Science."),
        ("STU-1005", "Evan Wright", 1.8, "REJECTED", "Academic probation history.")
    ]

    cursor.executemany("INSERT OR REPLACE INTO students VALUES (?, ?, ?, ?, ?)", students_data)

    conn.commit()
    conn.close()
    print("✅ Database 'university.db' created successfully with 5 records.")


if __name__ == "__main__":
    create_database()