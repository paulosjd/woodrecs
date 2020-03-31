**btk2**

REST API backend for a [web application](http://mysite.com) used to track individuals health metrics.

Third party libraries include Django 2.1, PyJWT, Django Rest Framework 3.5 and Celery 4.3. 
Configured to use Postgres for the database and Redis as the message broker for Celery tasks.

Quick start
-----------

    $ apt-get update
    $ apt-get install python3-pip python3-dev python3-venv nginx redis-server -y

1. Clone the repository and install requirements using `pip`

2. Run `python manage.py migrate` to create the database schema

3. Create a user with administrative permissions by running `python manage.py createsuperuser`
 and then use the admin views to manage records
 
Tasks require Redis to be installed and a server running.

Data can be loaded using `python manage.py loaddata <file_name>.json`



Permission numbers:

    0 = ---
    1 = --x
    2 = -w-
    3 = -wx
    4 = r-
    5 = r-x
    6 = rw-
    7 = rwx

`chmod 777 foldername` will give read, write, and execute permissions for everyone.

`chmod 700 foldername` will give read, write, and execute permissions for the user only.

`chmod 327 foldername` will give write and execute (3) permission for the user, w (2) for the group, and read, write, and execute for the users.

***

If there is a folder that is owned by user tomcat6:

    drwxr-xr-x 2 tomcat6 tomcat6 69632 2011-05-06 03:43 document

And I want to allow another user (ruser) write permissions on document folder. The two users (tomcat6 and ruser) does not belong to same group. 

There are two ways to do this: set the directory to "world" writable or create a new group for the two users and make the directory writeable to that group. The second option is preferable. Users in Linux can belong to more than one group. In this case you want to create a brand new group, let's call it `tomandruser`:

    sudo groupadd tomandruser

Now that the group exists, add the two users to it:

    sudo usermod -a -G tomandruser tomcat6
    sudo usermod -a -G tomandruser ruser

Now all that's left is to set the permissions on the directory:

    sudo chgrp -R tomandruser /path/to/the/directory
    sudo chmod -R 770 /path/to/the/directory

Now only members of the `tomandruser` group can read, write, or execute anything within the directory. Note the `-R` argument to the `chmod` and `chgrp` commands: this tells them to recurse into every sub directory of the target directory and modify every file and directory it finds.

You may also want to change `770` to something like `774` if you want others to be able to read the files, 775 if you want others to read and execute the files, etc. Group assignment changes won't take effect until the users log out and back in.

***

Granting 775 permissions on a directory doesn't automatically mean that all users in a certain group will gain `rwx` access to it. They need to either be the owner of the directory or to belong to the directory's group:

    $ ls -ld some_dir
    drwxrwxr-x 2 alex consult 4096 Feb 20 10:10 some_dir/
                  ^     ^
                  |     |_____ directory's group
                  |___________ directory's owner

So, in order to allow both alex and ben to have write access to `some_dir`, the `some_dir` directory itself must belong to the `consult` group. If that's not the case, the directory's owner (alex in this example), should issue the following command:

    $ chgrp consult some_dir/

Use `-R` flag to change group ownership of everything inside the directory:

    $ chgrp -R consult some_dir/

This will only work if alex is a member of the `consult` group

***
