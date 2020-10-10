"""Module for ingestion of image metadata."""

from configparser import ConfigParser
import os
import psycopg2
from PIL import Image


def generate_images(filename, sizes):
    """Create images."""
    exports = list()
    for size in sizes:
        image = Image.open(filename)
        image.thumbnail(size, Image.ANTIALIAS)
        tmp_name = filename[:filename.rfind('.')] + "(%i,%i)" % size
        image.save(tmp_name, "JPEG")
        exports.append(tmp_name)
    return exports


def delete_images(exports):
    """Remove images."""
    for file in exports:
        os.remove(file)


def ingest(psql_config, name, description, small_file=None, medium_file=None):
    """Ingest image metadata."""

    with open(small_file, "rb") as file:
        small_data = file.read()

    with open(medium_file, "rb") as file:
        medium_data = file.read()

    try:
        conn = psycopg2.connect(**psql_config)
        cur = conn.cursor()

        cur.execute(
            '''INSERT INTO "photos" (name, description, small_data, medium_data) '''
            '''VALUES (%s, %s, %s, %s);''', (name, description, small_data, medium_data)
        )

        conn.commit()
        cur.close()

    except psycopg2.DatabaseError as err:
        print(err)

    finally:
        if conn is not None:
            conn.close()


def upload(config_file, name, description, filename):
    """Upload image metadata into the PostgreSQL database."""

    # Dimension of images to be generated
    sizes = [(400, 300), (1280, 960)]

    # Create temporary images
    images = generate_images(filename, sizes)

    # Get postgresql config
    config = ConfigParser()
    config.read(config_file)
    postgresql_config = dict(config.items("postgresql"))

    # Add file contents to db
    ingest(postgresql_config, name, description, *images)

    # Remove temporary images
    delete_images(images)
