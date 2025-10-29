"""
Editor Widget Module

Custom text editor widget with @ mention dropdown functionality.
"""

import customtkinter as ctk
from typing import Optional, Callable
from .dropdown_menu import DropdownMenu


class EditorWidget(ctk.CTkTextbox):
    """Custom text editor with @ mention functionality"""

    def __init__(self, master, items: list, **kwargs):
        """
        Initialize the editor widget

        Args:
            master: Parent widget
            items: List of insertable items for the dropdown
            **kwargs: Additional arguments for CTkTextbox
        """
        super().__init__(master, **kwargs)

        self.insertable_items = items
        self.dropdown: Optional[DropdownMenu] = None
        self.at_position: Optional[str] = None

        # Initialize dropdown
        self._init_dropdown()

        # Bind events
        self._bind_events()

    def _init_dropdown(self):
        """Initialize the dropdown menu"""
        self.dropdown = DropdownMenu(
            parent_window=self.master,
            text_widget=self,
            items=self.insertable_items,
            on_select=self._on_item_selected,
        )

    def _bind_events(self):
        """Bind keyboard and mouse events"""
        # Bind key press to detect @ symbol
        self.bind("<KeyPress>", self._on_key_press)
        self.bind("<Key>", self._on_key)

        # Bind clicks to hide dropdown
        self.bind("<Button-1>", self._on_click)

        # Bind special keys for dropdown navigation
        self.bind("<Up>", self._on_up_arrow)
        self.bind("<Down>", self._on_down_arrow)
        self.bind("<Return>", self._on_return)
        self.bind("<Escape>", self._on_escape)

    def _on_key_press(self, event):
        """Handle key press events"""
        # Don't interfere with dropdown navigation
        if self.dropdown and self.dropdown.is_visible():
            if event.keysym in ["Up", "Down", "Return", "Escape"]:
                return

    def _on_key(self, event):
        """Handle key events to detect @ symbol"""
        # Check if @ was typed
        if event.char == "@":
            # Schedule dropdown display after the @ is inserted
            self.after(10, self._check_and_show_dropdown)

    def _check_and_show_dropdown(self):
        """Check if @ is present and show dropdown"""
        try:
            # Get current cursor position
            cursor_pos = self.index("insert")

            # Get the character before cursor
            char_before = self.get(f"{cursor_pos}-1c", cursor_pos)

            # If it's @, show the dropdown
            if char_before == "@":
                self.at_position = f"{cursor_pos}-1c"
                self._show_dropdown_at_cursor()
        except Exception as e:
            print(f"Error checking for @: {e}")

    def _show_dropdown_at_cursor(self):
        """Show the dropdown menu at the current cursor position"""
        try:
            cursor_pos = self.index("insert")
            bbox = self.bbox(cursor_pos)

            if bbox:
                x, y, width, height = bbox
                self.dropdown.show(x, y + height)
        except Exception as e:
            print(f"Error showing dropdown: {e}")

    def _on_item_selected(self, item: dict):
        """
        Handle item selection from dropdown

        Args:
            item: The selected item dict with 'insert' key
        """
        try:
            # Remove the @ symbol
            if self.at_position:
                cursor_pos = self.index("insert")
                self.delete(self.at_position, cursor_pos)

            # Insert the markdown element
            insert_text = item["insert"]
            self.insert("insert", insert_text)

            # Reset at position
            self.at_position = None

            # Focus back on editor
            self.focus_set()

        except Exception as e:
            print(f"Error inserting item: {e}")

    def _on_up_arrow(self, event):
        """Handle up arrow key"""
        if self.dropdown and self.dropdown.is_visible():
            self.dropdown.navigate_up()
            return "break"
        return None

    def _on_down_arrow(self, event):
        """Handle down arrow key"""
        if self.dropdown and self.dropdown.is_visible():
            self.dropdown.navigate_down()
            return "break"
        return None

    def _on_return(self, event):
        """Handle return/enter key"""
        if self.dropdown and self.dropdown.is_visible():
            self.dropdown.select_current()
            return "break"
        return None

    def _on_escape(self, event):
        """Handle escape key"""
        if self.dropdown and self.dropdown.is_visible():
            self.dropdown.hide()
            self.at_position = None
            return "break"
        return None

    def _on_click(self, event):
        """Handle mouse click"""
        # Hide dropdown when clicking in editor
        if self.dropdown and self.dropdown.is_visible():
            self.dropdown.hide()
            self.at_position = None

    def hide_dropdown(self):
        """Public method to hide the dropdown"""
        if self.dropdown:
            self.dropdown.hide()
        self.at_position = None

    def get_text(self) -> str:
        """Get all text from the editor"""
        return self.get("1.0", "end-1c")

    def set_text(self, text: str):
        """Set the text in the editor"""
        self.delete("1.0", "end")
        self.insert("1.0", text)

    def clear(self):
        """Clear all text from the editor"""
        self.delete("1.0", "end")
