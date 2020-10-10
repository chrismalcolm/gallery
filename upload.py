"""Upload photo script."""

import tkinter as tk
from tkinter.filedialog import askopenfilename
from functools import partial

from ingest import upload


class UploadInterface():
    """Class which allows a user to add a image to the database"""

    def __init__(self):
        self.root = tk.Tk()
        self.entries = list()

        self.string_input("name")
        self.string_input("description")
        self.file_input("photo")
        self.message("...")
        self.upload_button()

    def run(self):
        """Run the interface."""
        self.root.mainloop()

    def upload_data(self):
        """Upload data into database."""
        upload(
            config_file="config.ini",
            name=self.entries[0][1].get(),
            description=self.entries[1][1].get(),
            filename=self.entries[2][1].get()
        )
        self.upload_message.set("Successful")
        for entry in self.entries:
            entry[1].delete(0, tk.END)

    def message(self, initial_value):
        """Custom message on success of upload."""
        self.upload_message = tk.StringVar()
        self.upload_message.set(initial_value)
        self.label = tk.Label(self.root, textvariable=self.upload_message)
        self.label.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    def string_input(self, field):
        """String input field"""
        row = tk.Frame(self.root)
        lab = tk.Label(row, width=15, text=field, anchor='w')
        ent = tk.Entry(row)
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        lab.pack(side=tk.LEFT)
        ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        self.entries.append((field, ent))

    def file_input(self, field):
        """File input field."""
        row = tk.Frame(self.root)
        lab = tk.Label(row, width=15, text=field, anchor='w')
        ent = tk.Entry(row)
        but = tk.Button(self.root, text='Browse', command=partial(self.get_filename, ent))
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        lab.pack(side=tk.LEFT)
        ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        but.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        self.entries.append((field, ent))

    def upload_button(self):
        """Upload button."""
        show_btn = tk.Button(self.root, text='Upload', command=self.upload_data)
        show_btn.pack(side=tk.LEFT, padx=5, pady=5)

    @staticmethod
    def get_filename(ent):
        """Set the filenmae in the entry field."""
        ent.delete(0, tk.END)
        ent.insert(0, askopenfilename())


if __name__ == "__main__":
    APP = UploadInterface()
    APP.run()
