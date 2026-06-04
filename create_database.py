# create_database.py
# This script reads schema.sql and creates the SQLite database

import sqlite3
import os

# ── 1. CONNECT TO DATABASE ─────────────────────────────────────────
# If bluestock_mf.db doesn't exist, SQLite creates it automatically
conn = sqlite3.connect("bluestock_mf.db")
cursor = conn.cursor()
print("✅ Connected to database")

# ── 2. READ THE SCHEMA FILE ────────────────────────────────────────
with open("sql/schema.sql", "r", encoding="utf-8") as f:
    schema_sql = f.read()
print("✅ Schema file read")

# ── 3. RUN THE SQL ─────────────────────────────────────────────────
cursor.executescript(schema_sql)
conn.commit()
print("✅ All tables created successfully")

# ── 4. VERIFY TABLES WERE CREATED ─────────────────────────────────
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("\nTables in database:")
for table in tables:
    print(f"  - {table[0]}")

conn.close()
print("\n✅ Database ready!")