Crypt password changer
======================

Password change webapp for `crypt(3)` databases using SQLAlchemy and Flask

The app provides a simple web interface with the four essential fields
(username, old password, new password twice) and can handle any database
that can be used with SQLAlchemy (PostgreSQL, MySQL, Oracle, MSSQL,
SQLite, and others).

No cookies or session management is used, and SQLAlchemy is employed in
a way that avoids SQL injection by not using SQL directly. For producing
the password digest, `crypt(3)` is used with the scheme `$6$` which
produces SHA-512 based hashes, supported by at least Linux (glibc),
FreeBSD and Solaris.

Deployment
----------

The easiest way is to use a WSGI-compliant web server and point the
appropriate configuration directive to `apache.wsgi`.

Configuration
-------------

 - Copy the file `config.sample.json` to `config.json` and fill in the
   necessary fields.
 - `db_url` is the [SQLAlchemy URL][1] that usually contains the driver
   and host name, port number, username, password, file or database name
   used to access the database that contains the credentials
 - `table` is the name of the table that stores the credentials
 - `fields` must contain a dictionary with at least two keys, the strings
   associated with `username` and `password` are the names of the columns
   used to store usernames and crypt(3) passwords, respectively

  [1]: https://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls

Dependencies
------------

 - Python 2.x (tested on 2.7)
 - SQLAlchemy (and the appropriate driver for the target database)
 - Flask

License
-------

The whole project is available under MIT license, see `LICENSE.txt`.
