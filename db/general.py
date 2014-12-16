import sqlite3

DB_NAME = os.environ["SCRSH_DB_NAME"]

# WON'T work probably!!

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    create_tables_query = """
    CREATE TABLE IF NOT EXISTS urls (
        "url" TEXT NOT NULL,
        "added" REAL NOT NULL,
        "status" TEXT);

    CREATE TABLE IF NOT EXISTS screenshots (
        "id" INTEGER NOT NULL,
        "url" TEXT NOT NULL,
        "status" TEXT NOT NULL,
        "scheduled" REAL,
        "taken" REAL,
        "path" TEXT,
        "retries" INTEGER DEFAULT (0)
    );
    """

    c.execute(create_tables_query)

    conn.commit()
    c.close()
