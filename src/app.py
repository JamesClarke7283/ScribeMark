import customtkinter as ctk
from tkinter import filedialog, messagebox
import os


class MarkdownEditor(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ScribeMark - Markdown Editor")
        self.geometry("900x700")

        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Items available in the @ dropdown
        self.insertable_items = [
            ("# Heading 1", "# "),
            ("## Heading 2", "## "),
            ("### Heading 3", "### "),
            ("**Bold Text**", "**text**"),
            ("*Italic Text*", "*text*"),
            ("- Bullet List", "- "),
            ("1. Numbered List", "1. "),
            ("[ ] Checkbox", "- [ ] "),
            ("```Code Block```", "```\ncode\n```"),
            ("[Link](url)", "[text](url)"),
            ("![Image](url)", "![alt](url)"),
            ("> Blockquote", "> "),
            ("---Horizontal Rule---", "\n---\n"),
        ]

        # Variables for dropdown
        self.dropdown_window = None
        self.dropdown_listbox = None
        self.at_position = None

        self.current_file = None
        self.setup_ui()

    def setup_ui(self):
        # Toolbar
        toolbar = ctk.CTkFrame(self, height=50)
        toolbar.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        # Toolbar buttons
        btn_new = ctk.CTkButton(toolbar, text="New", width=80, command=self.new_file)
        btn_new.pack(side="left", padx=5, pady=5)

        btn_open = ctk.CTkButton(toolbar, text="Open", width=80, command=self.open_file)
        btn_open.pack(side="left", padx=5, pady=5)

        btn_save = ctk.CTkButton(toolbar, text="Save", width=80, command=self.save_file)
        btn_save.pack(side="left", padx=5, pady=5)

        btn_save_as = ctk.CTkButton(
            toolbar, text="Save As", width=80, command=self.save_file_as
        )
        btn_save_as.pack(side="left", padx=5, pady=5)

        # Info label
        self.info_label = ctk.CTkLabel(
            toolbar, text="Type @ to insert markdown elements", text_color="gray"
        )
        self.info_label.pack(side="right", padx=10)

        # Text editor
        self.text_editor = ctk.CTkTextbox(self, wrap="word", font=("Courier", 13))
        self.text_editor.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        # Bind events
        self.text_editor.bind("<KeyRelease>", self.on_key_release)
        self.text_editor.bind("<Button-1>", self.hide_dropdown)
        self.text_editor.bind("<Escape>", self.hide_dropdown)

        # Focus on editor
        self.text_editor.focus()

    def on_key_release(self, event):
        """Handle key release events to detect @ symbol"""
        # Get the character just typed
        cursor_pos = self.text_editor.index("insert")

        # Check if @ was just typed
        if event.char == "@":
            self.at_position = cursor_pos
            self.show_dropdown()
        elif self.dropdown_window and self.dropdown_window.winfo_exists():
            # Handle navigation in dropdown
            if event.keysym == "Down":
                self.navigate_dropdown(1)
                return "break"
            elif event.keysym == "Up":
                self.navigate_dropdown(-1)
                return "break"
            elif event.keysym == "Return":
                self.insert_selected_item()
                return "break"
            elif event.keysym == "Escape":
                self.hide_dropdown()
                return "break"
            else:
                # Check if we should close the dropdown (if user moved away or typed space)
                if event.char in [" ", "\n"] or event.keysym in [
                    "Left",
                    "Right",
                    "BackSpace",
                ]:
                    self.hide_dropdown()

    def show_dropdown(self):
        """Show the dropdown menu at cursor position"""
        # Hide existing dropdown if any
        self.hide_dropdown()

        # Get cursor position in pixels
        try:
            cursor_pos = self.text_editor.index("insert")
            bbox = self.text_editor.bbox(cursor_pos)

            if bbox:
                x, y, width, height = bbox

                # Get absolute position on screen
                text_x = self.text_editor.winfo_rootx()
                text_y = self.text_editor.winfo_rooty()

                # Create dropdown window
                self.dropdown_window = ctk.CTkToplevel(self)
                self.dropdown_window.overrideredirect(True)  # Remove window decorations
                self.dropdown_window.geometry(
                    f"300x250+{text_x + x}+{text_y + y + height}"
                )

                # Create listbox
                self.dropdown_listbox = ctk.CTkScrollableFrame(self.dropdown_window)
                self.dropdown_listbox.pack(fill="both", expand=True)

                # Populate with items
                for i, (display_text, _) in enumerate(self.insertable_items):
                    btn = ctk.CTkButton(
                        self.dropdown_listbox,
                        text=display_text,
                        command=lambda idx=i: self.insert_item(idx),
                        anchor="w",
                        fg_color="transparent",
                        hover_color=("gray70", "gray30"),
                    )
                    btn.pack(fill="x", padx=2, pady=1)

                # Lift the dropdown above other windows
                self.dropdown_window.lift()

        except Exception as e:
            print(f"Error showing dropdown: {e}")

    def hide_dropdown(self, event=None):
        """Hide the dropdown menu"""
        if self.dropdown_window:
            try:
                self.dropdown_window.destroy()
            except:
                pass
            self.dropdown_window = None
            self.dropdown_listbox = None
            self.at_position = None

    def navigate_dropdown(self, direction):
        """Navigate up or down in the dropdown"""
        # This is a simplified version - could be enhanced with proper selection highlighting
        pass

    def insert_selected_item(self):
        """Insert the currently selected item"""
        # For now, insert the first item
        if self.dropdown_window:
            self.insert_item(0)

    def insert_item(self, index):
        """Insert the selected item at cursor position"""
        if 0 <= index < len(self.insertable_items):
            _, insert_text = self.insertable_items[index]

            # Remove the @ symbol
            if self.at_position:
                self.text_editor.delete(self.at_position + "-1c", self.at_position)

            # Insert the markdown element
            self.text_editor.insert("insert", insert_text)

            # Hide dropdown
            self.hide_dropdown()

            # Focus back on editor
            self.text_editor.focus()

    def new_file(self):
        """Create a new file"""
        if messagebox.askyesno("New File", "Clear current content?"):
            self.text_editor.delete("1.0", "end")
            self.current_file = None
            self.title("ScribeMark - Markdown Editor")

    def open_file(self):
        """Open a markdown file"""
        filepath = filedialog.askopenfilename(
            title="Open Markdown File",
            filetypes=[
                ("Markdown files", "*.md"),
                ("Text files", "*.txt"),
                ("All files", "*.*"),
            ],
        )

        if filepath:
            try:
                with open(filepath, "r", encoding="utf-8") as file:
                    content = file.read()
                    self.text_editor.delete("1.0", "end")
                    self.text_editor.insert("1.0", content)
                    self.current_file = filepath
                    self.title(f"ScribeMark - {os.path.basename(filepath)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file:\n{e}")

    def save_file(self):
        """Save the current file"""
        if self.current_file:
            try:
                content = self.text_editor.get("1.0", "end-1c")
                with open(self.current_file, "w", encoding="utf-8") as file:
                    file.write(content)
                messagebox.showinfo("Success", "File saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{e}")
        else:
            self.save_file_as()

    def save_file_as(self):
        """Save the file with a new name"""
        filepath = filedialog.asksaveasfilename(
            title="Save Markdown File",
            defaultextension=".md",
            filetypes=[
                ("Markdown files", "*.md"),
                ("Text files", "*.txt"),
                ("All files", "*.*"),
            ],
        )

        if filepath:
            try:
                content = self.text_editor.get("1.0", "end-1c")
                with open(filepath, "w", encoding="utf-8") as file:
                    file.write(content)
                self.current_file = filepath
                self.title(f"ScribeMark - {os.path.basename(filepath)}")
                messagebox.showinfo("Success", "File saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{e}")


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
