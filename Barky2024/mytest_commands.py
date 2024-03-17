import pytest
import requests
from commands import (
    CreateBookmarksTableCommand,
    AddBookmarkCommand,
    ListBookmarksCommand,
    DeleteBookmarkCommand,
    ImportGitHubStarsCommand,
    EditBookmarkCommand,
    QuitCommand,
)
from database_manager import DatabaseManager


class TestCommands:
    def setup_method(self, method):
        """Setup method to prepare the test environment."""
        self.db = DatabaseManager("test_bookmarks.db")  # Use a separate test database

        # Ensure the bookmarks table is created before each test
        self.create_command = CreateBookmarksTableCommand(self.db)


    def teardown_method(self):
        """Teardown method to clean up after tests."""
        # Drop the bookmarks table to clean up the database
        self.db.drop_table("bookmarks")
        self.db.close()  # Don't forget to close the database connection

    def test_create_bookmarks_table(self):
        command = CreateBookmarksTableCommand(self.db)
        command.execute()


        assert self.db.does_table_exist("bookmarks")
        columns = self.db.get_columns("bookmarks")
        #assert columns == ["id", "title", "url", "notes", "date_added"]
        assert sorted(columns) == sorted(["id", "title", "url", "notes", "date_added"])
    # Other test methods...


class CreateBookmarksTableCommand:
    def __init__(self, db):
        self.db = db

    def execute(self):
        self.db.create_table("bookmarks", {
            "id": "integer primary key autoincrement",
            "title": "text not null",
            "url": "text not null",
            "notes": "text",
            "date_added": "text not null",
        })
        pass

    def test_add_bookmark(self):
        data = {"title": "Test Bookmark", "url": "https://example.com"}
        command = AddBookmarkCommand()
        result = command.execute(data)


        assert result == "Bookmark added!"
        bookmarks = self.db.select("bookmarks").fetchall()
        assert len(bookmarks) == 1
        assert bookmarks[0]["title"] == "Test Bookmark"
        assert bookmarks[0]["url"] == "https://example.com"

    def test_list_bookmarks(self):
        self.db.add("bookmarks", {"title": "Bookmark 1", "url": "https://example.com/1"})
        self.db.add("bookmarks", {"title": "Bookmark 2", "url": "https://example.com/2"})
        command = ListBookmarksCommand()
        bookmarks = command.execute()

        assert len(bookmarks) == 2
        assert bookmarks[0]["title"] == "Bookmark 1"
        assert bookmarks[1]["title"] == "Bookmark 2"

    def test_delete_bookmark(self):
        self.db.add("bookmarks", {"title": "Bookmark to Delete", "url": "https://delete.com"})
        bookmark_id = self.db.select("bookmarks", "id").fetchone()[0]
        command = DeleteBookmarkCommand()
        result = command.execute(bookmark_id)

        assert result == "Bookmark deleted!"
        bookmarks = self.db.select("bookmarks").fetchall()
        assert len(bookmarks) == 0

    def test_delete_bookmark_nonexistent(self):
        command = DeleteBookmarkCommand()
        with pytest.raises(ValueError):
            command.execute(123)  # Nonexistent bookmark ID

    def test_import_github_stars_command_stub(self):
        # Stub implementation for testing - replace with actual GitHub API calls if needed
        data = {"github_username": "test_user"}
        command = ImportGitHubStarsCommand()
        result = command.execute(data)
        assert result == "Imported 0 bookmarks from starred repos!"  # No mocked data

    # EditBookmarkCommand test (assuming update data is a dictionary)
    def test_edit_bookmark(self):
        self.db.add(
            "bookmarks", {"title": "Old Bookmark", "url": "https://oldexample.com"}
        )
        bookmark_id = self.db.select("bookmarks", "id").fetchone()[0]
        update_data = {"title": "Updated Bookmark"}
        command = EditBookmarkCommand()
        result = command.execute({"id": bookmark_id, "update": update_data})

        assert result == "Bookmark updated!"
        bookmark = self.db.select("bookmarks", where={"id": bookmark_id}).fetchone()
        assert bookmark["title"] == "Updated Bookmark"

    def test_edit_bookmark_nonexistent(self):
        command = EditBookmarkCommand()
        with pytest.raises(ValueError):
            command.execute({"id": 123, "update": {"title": "Nonexistent Bookmark"}})

    def test_quit_command(self):
        with pytest.raises(SystemExit):
            command = QuitCommand()
            command.execute()