# gallery
A web application for uploading and viewing photos

## WIP
Currently we have the basic web page layout set up.
The frames and photos appear in a grid with 3 columns.
Photos can be uploaded and viewed in the web page.
Clicking on a photo will give you a bigger view of it.

## TODO
* Create photo manager i.e. upload/ delete, swap order
* Support collections
* Add transitions between medium size photos
* General clean up code

## Usage

After you cd into the project folder:


* Setup the database tables and user
```bash
~$ sudo -u postgres psql -f setup.sql
```

* To run the server, cd into the folder an run
```bash
~$ python3 server.py
```

* For an interface to add images
```bash
~$  python3 upload.py
```

Webpage will appear on `localhost:8080`. Press Ctrl + Shift + R to refresh the page.
May need to restart server after uploading images.
