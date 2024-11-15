import tkinter as tk
from tkinter import ttk, font, messagebox
import json
from datetime import datetime
import os
import re

class Note:
    def __init__(self, title="Untitled Note", content=""):
        self.title = title
        self.content = content
        self.last_modified = datetime.now().isoformat()

class NoteList(tk.Frame):
    def __init__(self, parent, on_note_selected, on_note_deleted):
        super().__init__(parent, bg='#1b2838')
        self.on_note_selected = on_note_selected
        self.on_note_deleted = on_note_deleted
        
        header = tk.Frame(self, bg='#1b2838')
        header.pack(fill=tk.X, pady=(0, 10))
        
        title = tk.Label(header, text="NOTES", fg='#ffffff', bg='#1b2838', font=('Arial', 12, 'bold'))
        title.pack(side=tk.LEFT, padx=10)
        
        btn_container = tk.Frame(header, bg='#1b2838')
        btn_container.pack(side=tk.RIGHT, padx=5)
        
        self.add_btn = tk.Button(btn_container, text="+", command=self.add_note,
                               bg='#2a475e', fg='#ffffff', font=('Arial', 12),
                               width=2, relief=tk.FLAT)
        self.add_btn.pack(side=tk.LEFT, padx=2)
        
        self.delete_btn = tk.Button(btn_container, text="🗑", command=self.delete_selected_note,
                                  bg='#2a475e', fg='#ffffff', font=('Arial', 12),
                                  width=2, relief=tk.FLAT)
        self.delete_btn.pack(side=tk.LEFT, padx=2)
        
        self.notes_frame = tk.Frame(self, bg='#1b2838')
        self.notes_frame.pack(fill=tk.BOTH, expand=True)
        
        self.notes = []
        self.note_buttons = []
        self.selected_note = None

    def add_note(self):
        note = Note()
        self.notes.append(note)
        self.create_note_button(note)
        self.select_note(note)

    def create_note_button(self, note):
        btn = tk.Button(self.notes_frame, text=note.title, anchor='w',
                       bg='#2a475e', fg='#ffffff', font=('Arial', 10),
                       relief=tk.FLAT, command=lambda: self.select_note(note))
        btn.pack(fill=tk.X, padx=5, pady=1)
        self.note_buttons.append((note, btn))

    def select_note(self, note):
        self.selected_note = note
        for n, btn in self.note_buttons:
            btn.configure(bg='#2a475e' if n != note else '#3d6a8a')
        self.on_note_selected(note)

    def delete_selected_note(self):
        if self.selected_note and messagebox.askyesno("Delete Note", "Are you sure you want to delete this note?"):
            self.notes.remove(self.selected_note)
            for note, btn in self.note_buttons[:]:
                if note == self.selected_note:
                    btn.destroy()
                    self.note_buttons.remove((note, btn))
            self.on_note_deleted()
            if self.notes:
                self.select_note(self.notes[0])
            else:
                self.add_note()

    def update_note_title(self, note, title):
        for n, btn in self.note_buttons:
            if n == note:
                btn.configure(text=title)
                break

class Editor(tk.Frame):
    def __init__(self, parent, on_text_changed):
        super().__init__(parent, bg='#1b2838')
        self.on_text_changed = on_text_changed
        
        self.toolbar = tk.Frame(self, bg='#2a475e')
        self.toolbar.pack(fill=tk.X, pady=(0, 1))
        
        button_font = ('Arial', 14, 'bold')
        buttons = [
            ("B", self.toggle_bold, "Bold (Ctrl+B)"),
            ("I", self.toggle_italic, "Italic (Ctrl+I)"),
            ("U", self.toggle_underline, "Underline (Ctrl+U)"),
            ("</>", self.insert_code_block, "Code Block (Ctrl+K)"),
            ("=", self.calculate_formula, "Calculate (=)")
        ]
        
        for text, command, tooltip in buttons:
            btn = tk.Button(self.toolbar, text=text, command=command,
                          bg='#2a475e', fg='#ffffff', relief=tk.FLAT,
                          font=button_font, width=3, height=1)
            btn.pack(side=tk.LEFT, padx=2, pady=2)
            self.create_tooltip(btn, tooltip)
        
        self.text_editor = tk.Text(self, wrap=tk.WORD, bg='#171d25', fg='#ffffff',
                                 insertbackground='#ffffff', relief=tk.FLAT,
                                 font=('Consolas', 11), padx=10, pady=10)
        self.text_editor.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)
        
        self.text_editor.tag_configure('bold', font=('Consolas', 11, 'bold'))
        self.text_editor.tag_configure('italic', font=('Consolas', 11, 'italic'))
        self.text_editor.tag_configure('underline', underline=True)
        self.text_editor.tag_configure('code', background='#2a2e33', foreground='#e6db74')
        
        self.text_editor.bind('<<Modified>>', self.on_text_change)
        self.text_editor.bind('<KeyRelease>', self.on_key_release)
        self.text_editor.bind('<Control-b>', lambda e: self.toggle_bold())
        self.text_editor.bind('<Control-i>', lambda e: self.toggle_italic())
        self.text_editor.bind('<Control-u>', lambda e: self.toggle_underline())
        self.text_editor.bind('<Control-k>', lambda e: self.insert_code_block())

    def create_tooltip(self, widget, text):
        def show_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = tk.Label(tooltip, text=text, bg='#2a475e', fg='white',
                           relief='solid', borderwidth=1)
            label.pack()
            
            def hide_tooltip():
                tooltip.destroy()
            
            widget.tooltip = tooltip
            widget.after(2000, hide_tooltip)
        
        def hide_tooltip(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
        
        widget.bind('<Enter>', show_tooltip)
        widget.bind('<Leave>', hide_tooltip)

    def toggle_bold(self, event=None):
        self.toggle_tag('bold')
        return 'break'

    def toggle_italic(self, event=None):
        self.toggle_tag('italic')
        return 'break'

    def toggle_underline(self, event=None):
        self.toggle_tag('underline')
        return 'break'

    def toggle_tag(self, tag_name):
        try:
            if self.text_editor.tag_ranges(tk.SEL):
                ranges = self.text_editor.tag_ranges(tk.SEL)
                if tag_name in self.text_editor.tag_names(ranges[0]):
                    self.text_editor.tag_remove(tag_name, *ranges)
                else:
                    self.text_editor.tag_add(tag_name, *ranges)
        except tk.TclError:
            pass

    def insert_code_block(self, event=None):
        try:
            if self.text_editor.tag_ranges(tk.SEL):
                selected_text = self.text_editor.get(tk.SEL_FIRST, tk.SEL_LAST)
                self.text_editor.delete(tk.SEL_FIRST, tk.SEL_LAST)
                self.text_editor.insert(tk.INSERT, f"```\n{selected_text}\n```")
                start = self.text_editor.index(f"insert-{len(selected_text)+4}c")
                end = self.text_editor.index("insert-1c")
                self.text_editor.tag_add('code', start, end)
            else:
                self.text_editor.insert(tk.INSERT, "```\n\n```")
                start = self.text_editor.index("insert-3c")
                self.text_editor.mark_set(tk.INSERT, "insert-2c")
                end = self.text_editor.index("insert+1c")
                self.text_editor.tag_add('code', start, end)
        except tk.TclError:
            pass
        return 'break'

    def calculate_formula(self, event=None):
        try:
            if self.text_editor.tag_ranges(tk.SEL):
                selected_text = self.text_editor.get(tk.SEL_FIRST, tk.SEL_LAST)
            else:
                line = self.text_editor.get("insert linestart", "insert lineend")
                selected_text = line
            
            expression = selected_text.replace('=', '').strip()
            expression = re.sub(r'\s+', '', expression)
            
            try:
                result = eval(expression)
                formatted_result = f"{expression} = {result}"
                if self.text_editor.tag_ranges(tk.SEL):
                    self.text_editor.delete(tk.SEL_FIRST, tk.SEL_LAST)
                    self.text_editor.insert(tk.INSERT, formatted_result)
                else:
                    self.text_editor.delete("insert linestart", "insert lineend")
                    self.text_editor.insert("insert linestart", formatted_result)
            except:
                messagebox.showerror("Error", "Invalid formula")
        except tk.TclError:
            pass
        return 'break'

    def on_key_release(self, event):
        if event.char == '=' and not event.state & 0x4:
            self.calculate_formula()

    def get_content(self):
        return self.text_editor.get("1.0", tk.END)

    def set_content(self, content):
        self.text_editor.delete("1.0", tk.END)
        self.text_editor.insert("1.0", content)

    def on_text_change(self, event):
        content = self.get_content()
        title = content.split('\n')[0].strip() or "Untitled Note"
        self.on_text_changed(content, title)
        self.text_editor.edit_modified(False)

class BetterNotepad:
    def __init__(self, root):
        self.root = root
        self.root.title("Better Notepad")
        
        self.root.configure(bg='#1b2838')
        
        main_container = tk.Frame(root, bg='#1b2838')
        main_container.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)
        
        self.note_list = NoteList(main_container, self.on_note_selected, self.on_note_deleted)
        self.note_list.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 3))
        
        self.editor = Editor(main_container, self.on_text_changed)
        self.editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.load_notes()
        if not self.note_list.notes:
            self.note_list.add_note()

    def load_notes(self):
        try:
            if os.path.exists('notes.json'):
                with open('notes.json', 'r') as f:
                    notes_data = json.load(f)
                    for note_data in notes_data:
                        note = Note(note_data['title'], note_data['content'])
                        self.note_list.notes.append(note)
                        self.note_list.create_note_button(note)
        except:
            pass

    def save_notes(self):
        notes_data = [{'title': note.title, 'content': note.content}
                     for note in self.note_list.notes]
        with open('notes.json', 'w') as f:
            json.dump(notes_data, f)

    def on_note_selected(self, note):
        self.editor.set_content(note.content)

    def on_note_deleted(self):
        self.save_notes()

    def on_text_changed(self, content, title):
        if self.note_list.selected_note:
            self.note_list.selected_note.content = content
            self.note_list.selected_note.title = title
            self.note_list.update_note_title(self.note_list.selected_note, title)
            self.save_notes()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x600")
    app = BetterNotepad(root)
    root.mainloop()