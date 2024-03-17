

import os
import pytest
import sqlite3
from database_manager import DatabaseManager
from commands import (
    CreateBookmarksTableCommand,
    AddBookmarkCommand,
    ListBookmarksCommand,
    DeleteBookmarkCommand,
    ImportGitHubStarsCommand,
    EditBookmarkCommand,
    QuitCommand,
)

@pytest.fixture
def database_manager(tmp_path):
    # Use pytest's tmp_path fixture to create a temporary database file
    db_file = tmp_path / "test_bookmarks.db"
    dbm = DatabaseManager(str(db_file))
    yield dbm
    # No need for explicit __del__ call; use close() instead
    dbm.close()
    # File removal is handled by pytest's tmp_path fixture

def test_execute(database_manager):
    # Test code remains largely unchanged; just ensure proper setup and teardown
    database_manager.create_table(
        "bookmarks",
        {
            "id": "integer primary key autoincrement",
            "title": "text not null",
            "url": "text not null",
            "notes": "text",
            "date_added": "text not null",
        },
    )

    # Use database_manager's connection directly for test-specific SQL operations
    cursor = database_manager.connection.cursor()
    cursor.execute(
        "INSERT INTO bookmarks (title, url, notes, date_added) VALUES (?, ?, ?, ?)",
        ("Test bookmark", "http://www.example.com", "Test notes", "2022-01-01"),
    )
    database_manager.connection.commit()

    cursor.execute("SELECT * FROM bookmarks WHERE url IS NOT NULL")
    assert cursor.fetchone() is not None

    database_manager.drop_table("bookmarks")

def test_drop_table(database_manager):
    database_manager.create_table('bookmarks', {'id': 'integer', 'name': 'text'})
    database_manager.drop_table('bookmarks')

    with pytest.raises(sqlite3.OperationalError):
        database_manager.connection.execute('SELECT * FROM bookmarks')

def test_add():
    with sqlite3.connect(':memory:') as conn:
        db = DatabaseManager(':memory:')  # Assuming DatabaseManager can handle in-memory DBs

        # Create the bookmarks table
        db.create_table('bookmarks', {'id': 'INTEGER PRIMARY KEY', 'title': 'TEXT', 'url': 'TEXT', 'notes': 'TEXT', 'date_added': 'TEXT'})

        # Add test data to the database
        data = {
            'title': 'Test Title',
            'url': 'http://example.com',
            'notes': 'Test notes',
            'date_added': '2022-01-01'
        }
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        db.connection.execute(f'INSERT INTO bookmarks ({columns}) VALUES ({placeholders})', tuple(data.values()))
        db.connection.commit()

        # Query the database and verify that the test data was added correctly
        cursor = db.connection.cursor()
        cursor.execute('SELECT * FROM bookmarks WHERE title = ?', ('Test Title',))
        result = cursor.fetchone()
        expected = (1, 'Test Title', 'http://example.com', 'Test notes', '2022-01-01')
        assert result == expected
