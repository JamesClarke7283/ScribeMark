# ScribeMark

A modern, modular markdown text editor built with Python and customtkinter. Features an intuitive '@' mention system for quickly inserting markdown elements.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![customtkinter](https://img.shields.io/badge/customtkinter-latest-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Features

- 🎨 **Modern UI** - Clean, dark-mode interface built with customtkinter
- ⚡ **@ Mention System** - Type '@' to bring up a dropdown menu of markdown elements
- 📝 **Full Markdown Support** - Insert headings, lists, code blocks, links, and more
- 💾 **File Operations** - Open, save, and manage markdown files
- 🔧 **Modular Architecture** - Clean, maintainable codebase with separated concerns
- ⌨️ **Keyboard Navigation** - Navigate dropdown with arrow keys, Enter to select, Escape to close

## Quick Start

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ScribeMark.git
cd ScribeMark
```

2. Install dependencies:
```bash
pip install -e .
```

### Running the Application

#### Option 1: Using the run script
```bash
python run.py
```

#### Option 2: Using the module
```bash
python -m src.app
```

#### Option 3: After installation
```bash
quarttailwind
```

## Usage

### Basic Editing

- Type or paste markdown content into the editor
- Use the toolbar buttons to create new files, open existing ones, or save your work
- The editor supports all standard markdown syntax

### @ Mention System

1. Type the **@** symbol anywhere in your document
2. A dropdown menu will appear with markdown elements:
   - **Headings** (H1, H2, H3)
   - **Text formatting** (bold, italic, strikethrough)
   - **Lists** (bullet, numbered, checkboxes)
   - **Code blocks** (inline and multiline)
   - **Links and images**
   - **Blockquotes**
   - **Horizontal rules**

3. Navigate the dropdown:
   - **↑/↓** arrows to navigate
   - **Enter** to insert selected element
   - **Escape** to close dropdown
   - **Click** on any item to insert

### File Operations

- **New** (📄 New) - Create a new document
- **Open** (📁 Open) - Open an existing markdown file (.md, .txt)
- **Save** (💾 Save) - Save current document
- **Save As** (💾 Save As) - Save with a new filename

## Project Structure

```
ScribeMark/
├── src/
│   ├── __init__.py           # Package initializer
│   ├── app.py                # Main application window
│   ├── editor_widget.py      # Custom text editor with @ functionality
│   ├── dropdown_menu.py      # Dropdown menu component
│   ├── file_operations.py    # File I/O handlers
│   ├── markdown_items.py     # Markdown element definitions
│   └── logging.py            # Logging configuration
├── assets/                   # Images and resources
├── docs/                     # Documentation
├── run.py                    # Quick run script
├── pyproject.toml            # Project configuration
└── README.md                 # This file
```

## Module Overview

### `app.py`
Main application window that orchestrates all components. Handles window setup, toolbar creation, and coordinates between modules.

### `editor_widget.py`
Custom CTkTextbox widget that implements the @ mention functionality. Handles keyboard events and dropdown triggering.

### `dropdown_menu.py`
Reusable dropdown menu component that displays markdown options. Supports keyboard navigation and position management.

### `file_operations.py`
Manages all file I/O operations including open, save, and file dialog interactions.

### `markdown_items.py`
Centralized repository of markdown elements available for insertion. Easy to extend with new items.

## Development

### Installing Development Dependencies

```bash
pip install -e ".[dev]"
```

### Code Formatting

The project uses `black` and `isort` for code formatting:

```bash
# Format code
black src/
isort src/

# Type checking
mypy src/
```

### Adding New Markdown Elements

To add new markdown elements to the @ dropdown:

1. Open `src/markdown_items.py`
2. Add a new dictionary to the `INSERTABLE_ITEMS` list:

```python
{
    "display": "Display Text",
    "insert": "text to insert",
    "description": "Description of element"
}
```

## Roadmap

- [ ] Live markdown preview pane
- [ ] Syntax highlighting for markdown
- [ ] Custom themes support
- [ ] Export to HTML/PDF
- [ ] Split-screen editing
- [ ] Search and replace functionality
- [ ] Recent files menu
- [ ] Customizable keyboard shortcuts
- [ ] Plugin system

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

- Built with [customtkinter](https://github.com/TomSchimansky/CustomTkinter)
- Inspired by modern markdown editors like Notion and Obsidian

## Support

If you encounter any issues or have questions, please [open an issue](https://github.com/yourusername/ScribeMark/issues) on GitHub.