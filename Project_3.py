import sys
import sqlite3
import csv

def main():
    print("Processing with SQLite...", file=sys.stderr)

    # 1. Create an in-memory database
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    # 2. Create a table
    cursor.execute("CREATE TABLE fragments (start INTEGER, end INTEGER)")

    # 3. Read data and insert into DB
    #    We read in chunks/transactions for speed
    batch_data = []
    for line in sys.stdin:
        try:
            parts = line.split()
            # Only need start and end
            batch_data.append((int(parts[1]), int(parts[2])))
        except (IndexError, ValueError):
            continue
        
        if len(batch_data) > 100000:
            cursor.executemany("INSERT INTO fragments VALUES (?, ?)", batch_data)
            batch_data = []
    
    # Insert remaining
    if batch_data:
        cursor.executemany("INSERT INTO fragments VALUES (?, ?)", batch_data)
    
    conn.commit()

    # 4. Run the SQL Query to generate the Matrix
    #    We do the math (end-start) and aggregation (COUNT) inside SQL
    query = """
    SELECT 
        (start + end) / 2 as offset,
        (end - start) as length,
        COUNT(*) as count
    FROM fragments
    WHERE length > 0 AND length <= 1000
    GROUP BY offset, length
    ORDER BY offset, length
    """

    # 5. Print Header
    print("offset\tfragment_length\tcount")

    # 6. Execute and Print Results
    cursor.execute(query)
    for row in cursor.fetchall():
        print(f"{row[0]}\t{row[1]}\t{row[2]}")

    conn.close()

if __name__ == "__main__":
    main()