"""
Dropdown Menu Component

Handles the dropdown menu that appears when typing '@' in the editor.
"""

import customtkinter as ctk
from typing import Callable, Optional


class DropdownMenu:
    """A dropdown menu that appears at cursor position in the text editor"""

    def __init__(self, parent_window, text_widget, items: list, on_select: Callable):
        """
        Initialize the dropdown menu

        Args:
            parent_window: The parent CTk window
            text_widget: The text widget to attach to
            items: List of dict items with 'display' and 'insert' keys
            on_select: Callback function when an item is selected
        """
        self.parent_window = parent_window
        self.text_widget = text_widget
        self.items = items
        self.on_select = on_select

        self.dropdown_window: Optional[ctk.CTkToplevel] = None
        self.buttons = []
        self.selected_index = 0

    def show(self, x: int, y: int):
        """
        Show the dropdown menu at specified position

        Args:
            x: X position relative to text widget
            y: Y position relative to text widget
        """
        # Hide existing dropdown if any
        self.hide()

        # Get absolute screen position
        text_x = self.text_widget.winfo_rootx()
        text_y = self.text_widget.winfo_rooty()

        # Create dropdown window
        self.dropdown_window = ctk.CTkToplevel(self.parent_window)
        self.dropdown_window.overrideredirect(True)
        self.dropdown_window.attributes("-topmost", True)

        # Position the window
        dropdown_x = text_x + x
        dropdown_y = text_y + y + 20  # Offset below cursor

        # Create frame for items
        frame = ctk.CTkScrollableFrame(
            self.dropdown_window, width=280, height=min(240, len(self.items) * 35 + 10)
        )
        frame.pack(fill="both", expand=True, padx=2, pady=2)

        # Populate with items
        self.buttons = []
        for i, item in enumerate(self.items):
            btn = ctk.CTkButton(
                frame,
                text=item["display"],
                command=lambda idx=i: self._on_item_click(idx),
                anchor="w",
                fg_color="transparent",
                hover_color=("gray70", "gray30"),
                height=32,
                corner_radius=6,
            )
            btn.pack(fill="x", padx=2, pady=1)
            self.buttons.append(btn)

        # Set initial selection
        self.selected_index = 0
        self._update_selection()

        # Position window (do this after packing to get correct size)
        self.dropdown_window.update_idletasks()
        window_width = self.dropdown_window.winfo_reqwidth()
        window_height = self.dropdown_window.winfo_reqheight()

        # Adjust position if it would go off screen
        screen_width = self.parent_window.winfo_screenwidth()
        screen_height = self.parent_window.winfo_screenheight()

        if dropdown_x + window_width > screen_width:
            dropdown_x = screen_width - window_width - 10

        if dropdown_y + window_height > screen_height:
            dropdown_y = text_y + y - window_height - 5  # Show above cursor

        self.dropdown_window.geometry(f"+{dropdown_x}+{dropdown_y}")

    def hide(self):
        """Hide and destroy the dropdown menu"""
        if self.dropdown_window:
            try:
                self.dropdown_window.destroy()
            except:
                pass
            self.dropdown_window = None
            self.buttons = []
            self.selected_index = 0

    def is_visible(self) -> bool:
        """Check if dropdown is currently visible"""
        return self.dropdown_window is not None and self.dropdown_window.winfo_exists()

    def navigate_up(self):
        """Move selection up in the dropdown"""
        if not self.is_visible():
            return

        self.selected_index = (self.selected_index - 1) % len(self.items)
        self._update_selection()

    def navigate_down(self):
        """Move selection down in the dropdown"""
        if not self.is_visible():
            return

        self.selected_index = (self.selected_index + 1) % len(self.items)
        self._update_selection()

    def select_current(self):
        """Select the currently highlighted item"""
        if not self.is_visible():
            return

        self._on_item_click(self.selected_index)

    def _update_selection(self):
        """Update the visual selection highlight"""
        for i, btn in enumerate(self.buttons):
            if i == self.selected_index:
                btn.configure(fg_color=("gray75", "gray25"))
            else:
                btn.configure(fg_color="transparent")

    def _on_item_click(self, index: int):
        """Handle item click"""
        if 0 <= index < len(self.items):
            item = self.items[index]
            self.on_select(item)
            self.hide()
