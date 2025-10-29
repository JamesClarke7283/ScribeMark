"""
File Operations Module

Handles file operations like open, save, new, etc.
"""

import os
from tkinter import filedialog, messagebox
from typing import Optional, Tuple


class FileOperations:
    """Handles all file operations for the markdown editor"""

    def __init__(self):
        """Initialize file operations handler"""
        self.current_file: Optional[str] = None
        self.file_types = [
            ("Markdown files", "*.md"),
            ("Text files", "*.txt"),
            ("All files", "*.*"),
        ]

    def new_file(self, confirm: bool = True) -> bool:
        """
        Create a new file

        Args:
            confirm: Whether to ask for confirmation

        Returns:
            True if new file was created, False if cancelled
        """
        if confirm:
            result = messagebox.askyesno(
                "New File",
                "Clear current content and start a new file?",
            )
            if not result:
                return False

        self.current_file = None
        return True

    def open_file(self) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Open a markdown file

        Returns:
            Tuple of (success, content, filepath)
        """
        filepath = filedialog.askopenfilename(
            title="Open Markdown File",
            filetypes=self.file_types,
        )

        if not filepath:
            return False, None, None

        try:
            with open(filepath, "r", encoding="utf-8") as file:
                content = file.read()
                self.current_file = filepath
                return True, content, filepath
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open file:\n{e}")
            return False, None, None

    def save_file(self, content: str) -> bool:
        """
        Save the current file

        Args:
            content: The content to save

        Returns:
            True if save was successful, False otherwise
        """
        if self.current_file:
            return self._write_file(self.current_file, content)
        else:
            return self.save_file_as(content)

    def save_file_as(self, content: str) -> Tuple[bool, Optional[str]]:
        """
        Save the file with a new name

        Args:
            content: The content to save

        Returns:
            Tuple of (success, filepath)
        """
        filepath = filedialog.asksaveasfilename(
            title="Save Markdown File",
            defaultextension=".md",
            filetypes=self.file_types,
        )

        if not filepath:
            return False, None

        if self._write_file(filepath, content):
            self.current_file = filepath
            return True, filepath

        return False, None

    def _write_file(self, filepath: str, content: str) -> bool:
        """
        Write content to a file

        Args:
            filepath: Path to write to
            content: Content to write

        Returns:
            True if successful, False otherwise
        """
        try:
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(content)
            messagebox.showinfo("Success", "File saved successfully!")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file:\n{e}")
            return False

    def get_current_file(self) -> Optional[str]:
        """Get the current file path"""
        return self.current_file

    def get_current_filename(self) -> str:
        """Get the current filename without path"""
        if self.current_file:
            return os.path.basename(self.current_file)
        return "Untitled"

    def has_current_file(self) -> bool:
        """Check if there is a current file"""
        return self.current_file is not None

    def set_current_file(self, filepath: Optional[str]):
        """Set the current file path"""
        self.current_file = filepath
