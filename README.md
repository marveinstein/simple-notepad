# Simple Notepad

A lightweight desktop text editor built with Python and Tkinter for quick note-taking and editing.

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-4B8BBE)

## Overview

This project is a simple notepad-style application designed for writing, saving, opening, and editing text files with a clean desktop interface. It includes common editing tools such as undo/redo, cut/copy/paste, and a built-in search-and-replace panel.

## Features

- Create, open, and save text files
- Undo and redo edits
- Cut, copy, and paste text
- Search within the document
- Replace text and replace-all support
- Case-sensitive and exact-match search options
- Save prompts for unsaved changes
- Clean, lightweight desktop UI
- Keyboard shortcuts for common actions

## Screenshots

The application uses a minimal editor layout with a floating search panel and replace controls for quick document editing.

## Requirements

- Python 3.x
- Tkinter (included with most Python installations on Windows)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/notepad.git
   cd notepad
   ```

2. Run the app:

   ```bash
   python notepad.py
   ```

## Build Executable

To package the app into a standalone executable using PyInstaller:

```bash
pyinstaller notepad.spec
```

This generates a Windows executable according to the configuration in [notepad.spec](notepad.spec).

## Project Structure

```text
notepad/
├── notepad.py
├── notepad.spec
├── README.md
├── images/
│   └── notepad.ico
└── .gitignore
```

## Keyboard Shortcuts

| Action    | Shortcut |
| --------- | -------- |
| New note  | Ctrl + N |
| Open file | Ctrl + O |
| Save file | Ctrl + S |
| Undo      | Ctrl + Z |
| Redo      | Ctrl + Y |
| Cut       | Ctrl + X |
| Copy      | Ctrl + C |
| Paste     | Ctrl + V |
| Find      | Ctrl + F |
| Replace   | Ctrl + H |
| Exit      | Ctrl + Q |

## License

This project is open for personal and educational use. Add a license file if you want to publish it publicly with a formal project license.

## Notes

This app is intentionally lightweight and easy to extend. It can be expanded with features like tabs, syntax highlighting, file explorer integration, or a custom theme system.
