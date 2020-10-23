"""Photo Manager Application."""

from configparser import ConfigParser
import tkinter as tk
from tkinter.filedialog import askopenfilename

from functools import partial
import os

from src import database
from src import photo


class PhotoManager():
    """Tkinter Photo Manager class."""

    TITLE = "Photo Manager"
    WIDTH = 1024
    HEIGHT = 768

    def __init__(self, psql_config):

        self.psql_config = psql_config
        self.image = dict()

        root = tk.Tk()
        container = tk.Frame(root)
        canvas = tk.Canvas(container, width=self.WIDTH, height=self.HEIGHT)

        # Title
        tk.Label(container, text=self.TITLE, font='Helvetica 18 bold') \
        .pack(side=tk.TOP, fill=tk.Y, padx=15, pady=15)

        # Inputs
        inputs = tk.Frame(container, pady=40)

        tk.Label(inputs, text="Add a photo", font='Helvetica 12 bold') \
        .grid(row=0, column=1, sticky=tk.N, pady=9)

        tk.Label(inputs, text="Name").grid(row=1, sticky=tk.W)
        tk.Label(inputs, text="Description").grid(row=2, sticky=tk.W)
        tk.Label(inputs, text="Filename").grid(row=3, sticky=tk.W)

        self.name_entry = tk.Entry(inputs, width=50)
        self.desc_entry = tk.Entry(inputs, width=50)
        self.file_entry = tk.Entry(inputs, width=50)

        browse_command = partial(self.get_filename, self.file_entry)
        browse_button = tk.Button(inputs, text='Browse', command=browse_command)

        self.name_entry.grid(row=1, column=1, sticky=tk.W, padx=15, pady=9)
        self.desc_entry.grid(row=2, column=1, sticky=tk.W, padx=15, pady=9)
        self.file_entry.grid(row=3, column=1, sticky=tk.W, padx=15, pady=9)
        browse_button.grid(row=3, column=2, sticky=tk.W)

        tk.Button(inputs, text='Create', command=self.add_row) \
        .grid(row=4, column=1, sticky=tk.N)

        self.report = tk.StringVar()
        tk.Label(inputs, textvariable=self.report) \
        .grid(row=5, column=1, sticky=tk.N, pady=9)
        self.report.set("")

        inputs.pack(side=tk.TOP)

        # Scrollbar
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Table
        self.table = tk.Frame(canvas, pady=20)
        tk.Label(self.table, text="Manage photos", font='Helvetica 12 bold') \
        .pack(pady=15)

        self.table.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        canvas.create_window((0, 0), window=self.table, anchor="nw")

        row = tk.Frame(self.table)

        tk.Label(row, text="Id", width=10) \
        .grid(row=0, column=0, sticky=tk.W)
        tk.Label(row, text="Name", width=20, wraplength=150) \
        .grid(row=0, column=1, sticky=tk.W)
        tk.Label(row, text="Description", width=30, wraplength=240) \
        .grid(row=0, column=2, sticky=tk.W)
        tk.Label(row, text="Photo", width=50) \
        .grid(row=0, column=3, sticky=tk.W)
        tk.Label(row, text="", width=13) \
        .grid(row=0, column=4, sticky=tk.W)

        row.pack(pady=9)

        for uid, meta in self._configure_metadata():
            self.add_row(uid, meta)

        container.pack()
        canvas.pack(side="left", fill="both", expand=True)

        root.mainloop()

    def _configure_metadata(self):
        """Yield row metadata from the database."""
        query_params = (
            '''SELECT id, name, description, small_data, medium_data FROM photos;''',
        )
        results = database.postgresql_query(self.psql_config, query_params)
        for entry in results[0]:
            yield (
                int(entry[0]),
                {
                    "name": str(entry[1]),
                    "description": str(entry[2]),
                    "small_data": bytes(entry[3]),
                    "medium_data": bytes(entry[4])
                }
            )

    def add_row(self, uid=None, meta=None):
        """
            Add a row in the table.

            Parameters:
            > uid (int) - the unique ID of the row in the database
            > meta (dict) - mapping of row metadata

            NB: The success of the addition is stated in self.report
        """
        meta = meta or dict()

        # Get metadata if any
        name = meta.get("name", "")
        description = meta.get("description", "")
        data = meta.get("medium_data", b'')
        scale = 4

        # If no id is given
        # Extract metadata from interface and upload new row to database
        if uid is None:
            name = self.name_entry.get()
            description = self.desc_entry.get()
            filename = self.file_entry.get()
            results, errors = self.upload(name, description, filename)
            if errors:
                self.report.set("Errors occurred: " + ", ".join(errors))
                print("Debug", errors)
                return
            with open(filename, "rb") as file:
                data = file.read()
            scale = 16
            uid = results[0][0]
            self.report.set("Successfully added, row %i" % uid)

        # Create image
        self.image[uid] = photo.tk_image(data, scale)

        # Create row
        row = tk.Frame(self.table)

        tk.Label(row, text=str(uid), width=10) \
        .grid(row=0, column=0, sticky=tk.W)
        tk.Label(row, text=name, width=20, wraplength=150) \
        .grid(row=0, column=1, sticky=tk.W)
        tk.Label(row, text=description, width=30, wraplength=240) \
        .grid(row=0, column=2, sticky=tk.W)
        tk.Label(row, image=self.image[uid], width=400) \
        .grid(row=0, column=3, sticky=tk.W)

        delete_command = partial(self.delete_row, uid, row)
        tk.Button(row, text='Delete', command=delete_command, width=10) \
        .grid(row=0, column=4, sticky=tk.W)

        row.pack()

    def delete_row(self, uid, row):
        """
            Remove a row in the table and in the database.

            Parameters:
            > uid (int) - the unique ID of the row in the database
            > row (tkinter.Frame) - the tkinter row object to be removed

            NB: The success of the deletion is stated in self.report
        """
        query_params = ('''DELETE FROM photos WHERE id = %i RETURNING id;''' % (uid),)
        _, errors = database.postgresql_query(self.psql_config, query_params, commit=True)
        if errors:
            self.report.set("Error deleting row %i" % uid)
            print("Debug", errors)
        else:
            row.destroy()
            self.report.set("Successfully deleted row with id %i" % uid)

    @staticmethod
    def get_filename(ent):
        """Set the filenmae in the entry field."""
        ent.delete(0, tk.END)
        ent.insert(0, askopenfilename())

    def upload(self, name, description, filename):
        """Upload image metadata into the PostgreSQL database."""

        results = None
        errors = list()

        # Errors with empty/incorrect variables
        if not name:
            errors.append("Name is empty")
        if not description:
            errors.append("Description is empty")
        if not filename:
            errors.append("Filename is empty")
        if errors:
            return results, errors

        # Create temporary images
        small_file = filename[:filename.rfind('.')] + "(small)"
        medium_file = filename[:filename.rfind('.')] + "(medium)"

        try:
            photo.resize_image(filename, small_file, (400, 300))
            photo.resize_image(filename, medium_file, (1280, 960))
        except FileNotFoundError:
            errors.append("File %s not found" % filename)

        with open(small_file, "rb") as file:
            small_data = file.read()

        with open(medium_file, "rb") as file:
            medium_data = file.read()

        results, errors = database.postgresql_query(
            self.psql_config,
            (
                '''INSERT INTO "photos" (name, description, small_data, medium_data) '''
                '''VALUES (%s, %s, %s, %s) RETURNING id;'''
                '''''', (name, description, small_data, medium_data)
            ),
            commit=True
        )

        try:
            os.remove(small_file)
        except FileNotFoundError:
            errors.append("Warning: Unable to remove %s" % small_file)

        try:
            os.remove(medium_file)
        except FileNotFoundError:
            errors.append("Warning: Unable to remove %s" % medium_file)

        return results, errors


def main(config_file):
    """Run the Photo Manager application."""

    # Get server and postgresql config
    config = ConfigParser()
    config.read(config_file)
    postgresql_config = dict(config.items("postgresql"))

    # Run the photo manager
    PhotoManager(postgresql_config)


if __name__ == "__main__":
    main("config.ini")
