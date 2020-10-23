# My Gallery
A web application for uploading and viewing photos.

## Usage
This project allows you to add/delete photos in a PostgreSQL database
and view the photos in a web application.

After downloading this repo locally using the `git clone`command,
cd into the project folder:

* Setup the database tables and user
```bash
~$ sudo -u postgres psql -f setup.sql
```

* To run the server
```bash
~$ python3 server.py
```

* For an interface to add and delete images
```bash
~$  python3 manager.py
```

Webpage will appear on `localhost:8080`.
This address can be changed in the config.

Press Ctrl + Shift + R to refresh the page.
May need to restart server after uploading images.

## TODO
* Support collections (sub galleries)
* Add transitions between photos on main webpage
* Support horizontal images
* Support varying sizes for images
