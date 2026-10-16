import tkinter as tk
from tkinter import Text, Tk, Frame, Menu, filedialog, messagebox


# Save the editor contents to a file chosen by the user.
def save_note():
    note_content = text_area.get("1.0", "end-1c")
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
    )
    if file_path:
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(note_content)
            text_area.edit_modified(False)
            messagebox.showinfo("Success", "Note saved successfully!")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save note: {e}")
    return False


# Load a text file into the editor.
def load_note():
    file_path = filedialog.askopenfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
    )
    if file_path:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                note_content = file.read()
            text_area.delete("1.0", tk.END)
            text_area.insert(tk.END, note_content)
            text_area.edit_modified(False)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load note: {e}")


# Confirm whether to save nonempty text before starting a new note.
def new_note():
    if text_area.get("1.0", "end-1c"):
        save_changes = messagebox.askyesnocancel(
            "Unsaved Changes", "Save changes before creating a new note?"
        )
        if save_changes is None:
            return
        if save_changes and not save_note():
            return

    text_area.delete("1.0", tk.END)
    text_area.edit_modified(False)


# Prompt to save unsaved edits before closing the window.
def close_app(event=None):
    if text_area.edit_modified():
        save_changes = messagebox.askyesnocancel(
            "Unsaved Changes", "Save changes before closing?"
        )
        if save_changes is None:
            return
        if save_changes and not save_note():
            return
    root.destroy()


# Undo the most recent text edit when one is available.
def undo():
    try:
        text_area.edit_undo()
    except tk.TclError:
        pass


# Redo the most recently undone text edit when one is available.
def redo():
    try:
        text_area.edit_redo()
    except tk.TclError:
        pass


search_matches = []
current_match = -1


# Return the ranges where the query matches the current search options.
def get_search_matches(query):
    matches = []
    index = "1.0"
    while query:
        match = text_area.search(
            query,
            index,
            stopindex=tk.END,
            nocase=not match_case_var.get(),
        )
        if not match:
            break

        end = f"{match}+{len(query)}c"
        if exact_match_var.get():
            previous_char = text_area.get(f"{match} - 1c", match)
            next_char = text_area.get(end, f"{end}+1c")
            if (
                previous_char and (previous_char.isalnum() or previous_char == "_")
            ) or (next_char and (next_char.isalnum() or next_char == "_")):
                index = f"{match}+1c"
                continue

        matches.append((match, end))
        index = end
    return matches


# Refresh highlighted matches and the search result count.
def update_search_highlights(*_):
    global search_matches, current_match
    text_area.tag_remove("search_match", "1.0", tk.END)
    text_area.tag_remove("current_search_match", "1.0", tk.END)
    current_match = -1
    query = search_entry.get()
    search_matches = get_search_matches(query)
    for start, end in search_matches:
        text_area.tag_add("search_match", start, end)
    result_label.config(
        text=f"{len(search_matches)} results" if search_matches else "No results"
    )


# Select and scroll to the next or previous search match.
def find_text(direction=1):
    global current_match
    if not search_matches:
        update_search_highlights()
    if not search_matches:
        return

    if current_match < 0:
        current_match = 0 if direction > 0 else len(search_matches) - 1
    else:
        current_match = (current_match + direction) % len(search_matches)

    start, end = search_matches[current_match]
    text_area.tag_remove("current_search_match", "1.0", tk.END)
    text_area.tag_add("current_search_match", start, end)
    text_area.tag_remove("sel", "1.0", tk.END)
    text_area.tag_add("sel", start, end)
    text_area.mark_set("insert", end)
    text_area.see(start)
    result_label.config(text=f"{current_match + 1} of {len(search_matches)}")


# Advance to the next match when Enter is pressed in the search field.
def find_next_from_entry(event=None):
    find_text()
    return "break"


# Advance to the previous match when Shift+Enter is pressed.
def find_previous_from_entry(event=None):
    find_previous()
    return "break"


# Navigate to the previous search match.
def find_previous():
    find_text(-1)


# Replace the selected match and move to the next one.
def replace_next():
    query = search_entry.get()
    if not query:
        return

    selection = text_area.tag_ranges("sel")
    if selection:
        selected_range = (text_area.index(selection[0]), text_area.index(selection[1]))
        if selected_range in search_matches:
            text_area.delete(*selection)
            text_area.insert("insert", replacement_entry.get())
            update_search_highlights()

    find_text()


# Replace every match in the editor.
def replace_all():
    query = search_entry.get()
    if not query:
        return

    replacement = replacement_entry.get()
    for start, end in reversed(get_search_matches(query)):
        text_area.delete(start, end)
        text_area.insert(start, replacement)

    update_search_highlights()


# Position a window at the center of the screen.
def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    window.geometry(f"{width}x{height}+{x}+{y}")


# Display the search panel at the upper-right of the main window.
def show_search_window():
    root.update_idletasks()
    search_panel.place(relx=1.0, x=-12, y=12, anchor="ne")
    search_panel.lift()


# Hide the search panel and return focus to the editor.
def hide_search_window(event=None):
    search_panel.place_forget()
    text_area.focus_set()
    return "break"


# Show or hide the replace controls in the search panel.
def toggle_replace(show=None):
    if show is None:
        show = not replace_row.winfo_ismapped()
    if show:
        replace_row.grid()
    else:
        replace_row.grid_remove()


# Open the search panel and focus its query field.
def focus_find(event=None):
    show_search_window()
    toggle_replace(False)
    search_entry.focus_set()
    search_entry.selection_range(0, tk.END)
    return "break"


# Open the search panel and focus its replacement field.
def focus_replace(event=None):
    show_search_window()
    toggle_replace(True)
    replacement_entry.focus_set()
    replacement_entry.selection_range(0, tk.END)
    return "break"


root = Tk()
root.title("Notepad")
root.geometry("600x450")

root.iconbitmap("images/notepad.ico")

menubar = Menu(root)
root.config(menu=menubar)

file_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=file_menu, underline=0)
file_menu.add_command(label="New", command=new_note, underline=0, accelerator="Ctrl+N")
file_menu.add_command(
    label="Open", command=load_note, underline=0, accelerator="Ctrl+O"
)
file_menu.add_command(
    label="Save", command=save_note, underline=0, accelerator="Ctrl+S"
)
file_menu.add_separator()
file_menu.add_command(
    label="Exit", command=close_app, underline=1, accelerator="Ctrl+Q"
)

edit_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Edit", menu=edit_menu, underline=0)
edit_menu.add_command(label="Undo", command=undo, underline=0, accelerator="Ctrl+Z")
edit_menu.add_command(label="Redo", command=redo, underline=0, accelerator="Ctrl+Y")
edit_menu.add_separator()
edit_menu.add_command(
    label="Cut",
    command=lambda: text_area.event_generate("<<Cut>>"),
    underline=2,
    accelerator="Ctrl+X",
)
edit_menu.add_command(
    label="Copy",
    command=lambda: text_area.event_generate("<<Copy>>"),
    underline=0,
    accelerator="Ctrl+C",
)
edit_menu.add_command(
    label="Paste",
    command=lambda: text_area.event_generate("<<Paste>>"),
    underline=0,
    accelerator="Ctrl+V",
)
edit_menu.add_separator()
edit_menu.add_command(
    label="Find", command=focus_find, underline=0, accelerator="Ctrl+F"
)
edit_menu.add_command(
    label="Replace", command=focus_replace, underline=3, accelerator="Ctrl+H"
)

search_panel = tk.Frame(root, padx=6, pady=6, relief=tk.SOLID, borderwidth=1)
search_text = tk.StringVar()
search_entry = tk.Entry(search_panel, width=22, textvariable=search_text)
search_entry.grid(row=0, column=0, padx=3, pady=3)
search_text.trace_add("write", update_search_highlights)
search_entry.bind("<Return>", find_next_from_entry)
search_entry.bind("<Shift-Return>", find_previous_from_entry)

search_text = tk.StringVar()

search_input = tk.Frame(search_panel, relief=tk.SOLID, borderwidth=1)
search_input.grid(row=0, column=0, columnspan=3, padx=3, pady=3, sticky="ew")

search_entry = tk.Entry(
    search_input, width=18, textvariable=search_text, relief=tk.FLAT
)
search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=4)
search_text.trace_add("write", update_search_highlights)
search_entry.bind("<Return>", find_next_from_entry)
search_entry.bind("<Shift-Return>", find_previous_from_entry)

exact_match_var = tk.BooleanVar(value=False)
tk.Checkbutton(
    search_input,
    text="ab",
    variable=exact_match_var,
    command=update_search_highlights,
    indicatoron=False,
    width=3,
).pack(side=tk.LEFT, padx=1)

match_case_var = tk.BooleanVar(value=False)
tk.Checkbutton(
    search_input,
    text="Aa",
    variable=match_case_var,
    command=update_search_highlights,
    indicatoron=False,
    width=3,
).pack(side=tk.LEFT, padx=1)

exact_match_var = tk.BooleanVar(value=False)
match_case_var = tk.BooleanVar(value=False)
tk.Checkbutton(
    search_panel,
    text="Aa",
    variable=exact_match_var,
    command=update_search_highlights,
    indicatoron=False,
    width=3,
).grid(row=0, column=1, padx=2, pady=3)
tk.Checkbutton(
    search_panel,
    text="ab",
    variable=match_case_var,
    command=update_search_highlights,
    indicatoron=False,
    width=3,
).grid(row=0, column=2, padx=2, pady=3)
tk.Button(search_panel, text="\u2190", command=find_previous).grid(
    row=0, column=3, padx=2, pady=3
)
tk.Button(search_panel, text="\u2192", command=find_text).grid(
    row=0, column=4, padx=2, pady=3
)
result_label = tk.Label(search_panel, text="No results", width=10)
result_label.grid(row=0, column=5, padx=3, pady=3)
tk.Button(search_panel, text="\u25bc", command=toggle_replace).grid(
    row=0, column=6, padx=2, pady=3
)
tk.Button(search_panel, text="X", command=hide_search_window, width=2).grid(
    row=0, column=7, padx=2, pady=3
)

replace_row = tk.Frame(search_panel)
replace_row.grid(row=1, column=0, columnspan=8, sticky="ew")
replacement_entry = tk.Entry(replace_row, width=22)
replacement_entry.grid(row=0, column=0, padx=3, pady=3)
tk.Button(replace_row, text="Replace", command=replace_next).grid(
    row=0, column=1, padx=2, pady=3
)
tk.Button(replace_row, text="Replace All", command=replace_all).grid(
    row=0, column=2, padx=2, pady=3
)
replace_row.grid_remove()

text_area = Text(root, padx=10, pady=10, undo=True, wrap=tk.WORD)
text_area.tag_configure("search_match", background="yellow", foreground="black")
text_area.tag_configure(
    "current_search_match", background="#a8d7ff", foreground="black"
)
text_area.pack(fill=tk.BOTH, expand=True)
root.after_idle(text_area.focus_set)

root.bind("<Control-n>", lambda event: new_note())
root.bind("<Control-o>", lambda event: load_note())
root.bind("<Control-s>", lambda event: save_note())
root.bind("<Control-q>", close_app)
root.bind("<Control-f>", focus_find)
root.bind("<Control-h>", focus_replace)
root.bind("<Escape>", hide_search_window)

root.protocol("WM_DELETE_WINDOW", close_app)
center_window(root)
root.mainloop()
