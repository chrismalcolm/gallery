"""This module contains useful tools for dealing with image files."""

from PIL import Image, ImageTk


def resize_image(source, destination, dimensions, extension="JPEG"):
    """
        Creates a copy of the image file 'source' at the file location
        'destination' with the given 'dimensions'.

        Parameters:
        > source (str) - filename of the original image
        > destination (str) - location of the copied image
        > dimensions (tuple) - the (width, height) of the copied image
        > extension (str) - image file extension
    """
    image = Image.open(source)
    image.thumbnail(dimensions, Image.ANTIALIAS)
    image.save(destination, extension)


def tk_image(data, scale):
    """
        Creates an image object which can be used in a tk interface.

        Parameters:
        > data (bytes) - raw image byte data
        > scale (int) - the image sample is scaled by (1 / scale)

        Returns:
        > (tkinter.PhotoImage) - scaled tk interface friendly image
    """
    image = ImageTk.PhotoImage(data=data)
    return image._PhotoImage__photo.subsample(scale)
