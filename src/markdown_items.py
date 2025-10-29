"""
Markdown Items Module

Contains predefined markdown elements that can be inserted into the editor.
"""

INSERTABLE_ITEMS = [
    {"display": "# Heading 1", "insert": "# ", "description": "Large heading"},
    {"display": "## Heading 2", "insert": "## ", "description": "Medium heading"},
    {"display": "### Heading 3", "insert": "### ", "description": "Small heading"},
    {
        "display": "**Bold Text**",
        "insert": "**text**",
        "description": "Bold formatting",
    },
    {
        "display": "*Italic Text*",
        "insert": "*text*",
        "description": "Italic formatting",
    },
    {"display": "- Bullet List", "insert": "- ", "description": "Unordered list item"},
    {
        "display": "1. Numbered List",
        "insert": "1. ",
        "description": "Ordered list item",
    },
    {
        "display": "[ ] Checkbox",
        "insert": "- [ ] ",
        "description": "Task list checkbox",
    },
    {
        "display": "```Code Block```",
        "insert": "```\ncode\n```",
        "description": "Code block",
    },
    {"display": "[Link](url)", "insert": "[text](url)", "description": "Hyperlink"},
    {"display": "![Image](url)", "insert": "![alt](url)", "description": "Image embed"},
    {"display": "> Blockquote", "insert": "> ", "description": "Quote block"},
    {
        "display": "---Horizontal Rule---",
        "insert": "\n---\n",
        "description": "Horizontal divider",
    },
    {"display": "`Inline Code`", "insert": "`code`", "description": "Inline code"},
    {
        "display": "~~Strikethrough~~",
        "insert": "~~text~~",
        "description": "Strikethrough text",
    },
]


def get_items():
    """Return the list of insertable markdown items"""
    return INSERTABLE_ITEMS


def get_item_display_texts():
    """Return just the display texts"""
    return [item["display"] for item in INSERTABLE_ITEMS]


def get_item_insert_texts():
    """Return just the insert texts"""
    return [item["insert"] for item in INSERTABLE_ITEMS]
