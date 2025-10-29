"""
ScribeMark - Markdown Text Editor
Main application module
"""

import customtkinter as ctk
import os
from .editor_widget import EditorWidget
from .file_operations import FileOperations
from .markdown_items import get_items


class MarkdownEditor(ctk.CTk):
    """Main application window for ScribeMark"""

    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("ScribeMark - Markdown Editor")
        self.geometry("1000x700")
        self.minsize(800, 600)

        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Initialize file operations
        self.file_ops = FileOperations()

        # Setup UI
        self.setup_ui()

        # Bind window close event
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_ui(self):
        """Setup the user interface"""
        self.create_toolbar()
        self.create_editor()
        self.update_title()

    def create_toolbar(self):
        """Create the toolbar with file operation buttons"""
        toolbar = ctk.CTkFrame(self, height=60, corner_radius=0)
        toolbar.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        toolbar.grid_columnconfigure(4, weight=1)

        # New file button
        btn_new = ctk.CTkButton(
            toolbar,
            text="📄 New",
            width=100,
            height=36,
            command=self.new_file,
            corner_radius=8,
        )
        btn_new.grid(row=0, column=0, padx=10, pady=12)

        # Open file button
        btn_open = ctk.CTkButton(
            toolbar,
            text="📁 Open",
            width=100,
            height=36,
            command=self.open_file,
            corner_radius=8,
        )
        btn_open.grid(row=0, column=1, padx=5, pady=12)

        # Save file button
        btn_save = ctk.CTkButton(
            toolbar,
            text="💾 Save",
            width=100,
            height=36,
            command=self.save_file,
            corner_radius=8,
        )
        btn_save.grid(row=0, column=2, padx=5, pady=12)

        # Save As button
        btn_save_as = ctk.CTkButton(
            toolbar,
            text="💾 Save As",
            width=100,
            height=36,
            command=self.save_file_as,
            corner_radius=8,
        )
        btn_save_as.grid(row=0, column=3, padx=5, pady=12)

        # Info label
        self.info_label = ctk.CTkLabel(
            toolbar,
            text="💡 Type @ to insert markdown elements",
            text_color=("gray50", "gray60"),
            font=("", 12),
        )
        self.info_label.grid(row=0, column=4, padx=20, pady=12, sticky="e")

    def create_editor(self):
        """Create the main text editor"""
        # Container frame
        editor_frame = ctk.CTkFrame(self, corner_radius=0)
        editor_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        editor_frame.grid_rowconfigure(0, weight=1)
        editor_frame.grid_columnconfigure(0, weight=1)

        # Create editor widget with insertable items
        self.editor = EditorWidget(
            editor_frame,
            items=get_items(),
            wrap="word",
            font=("Courier New", 13),
            corner_radius=8,
        )
        self.editor.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Focus on editor
        self.editor.focus_set()

    def new_file(self):
        """Create a new file"""
        if self.file_ops.new_file(confirm=True):
            self.editor.clear()
            self.update_title()

    def open_file(self):
        """Open an existing file"""
        success, content, filepath = self.file_ops.open_file()
        if success and content is not None:
            self.editor.set_text(content)
            self.update_title()

    def save_file(self):
        """Save the current file"""
        content = self.editor.get_text()
        success = self.file_ops.save_file(content)
        if success:
            self.update_title()

    def save_file_as(self):
        """Save file with a new name"""
        content = self.editor.get_text()
        success, filepath = self.file_ops.save_file_as(content)
        if success:
            self.update_title()

    def update_title(self):
        """Update the window title with current filename"""
        filename = self.file_ops.get_current_filename()
        self.title(f"ScribeMark - {filename}")

    def on_closing(self):
        """Handle window close event"""
        # Could add unsaved changes check here
        self.destroy()


def main():
    """Main entry point for the application"""
    # Set appearance mode and color theme
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # Create and run the app
    app = MarkdownEditor()
    app.mainloop()


if __name__ == "__main__":
    main()
