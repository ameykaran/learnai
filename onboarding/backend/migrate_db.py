#!/usr/bin/env python3
"""
Database migration script to add new columns for improved adaptive algorithm.
"""

import sqlite3

def migrate_database():
    """Add new columns to quiz_sessions table for improved algorithm."""
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()

    # Check current schema
    cursor.execute("PRAGMA table_info(quiz_sessions)")
    columns = [row[1] for row in cursor.fetchall()]
    print(f"Current columns: {columns}")

    # Add new columns if they don't exist
    new_columns = [
        ('ability', 'REAL DEFAULT 0.25'),
        ('asked_ids', 'TEXT DEFAULT "[]"'),
        ('medium_seen', 'INTEGER DEFAULT 0'),
        ('difficult_seen', 'INTEGER DEFAULT 0'),
        ('history', 'TEXT DEFAULT "[]"'),
        ('final_ability', 'REAL')
    ]

    for column_name, column_def in new_columns:
        if column_name not in columns:
            try:
                cursor.execute(f"ALTER TABLE quiz_sessions ADD COLUMN {column_name} {column_def}")
                print(f"Added column: {column_name}")
            except sqlite3.Error as e:
                print(f"Error adding column {column_name}: {e}")

    conn.commit()
    conn.close()
    print("Database migration completed!")

if __name__ == "__main__":
    migrate_database()