Todotxt-cli
===========

Python cli for manage todolist



Installation
------------

::

    pip install todotxt-cli
        
Or

::

    git clone https://github.com/fraoustin/todotxt-cli.git
    cd todotxt-cli
    python setup.py install

You can load test by

::

    python -m unittest discover -s test

Usage
-----

::

    >> todo
    Usage: todo [OPTIONS] COMMAND [ARGS]...

    Options:
        -vv, --verbose
        -c, --conf FILENAME
        --version            Show the version and exit.
        --help               Show this message and exit.

    Commands:
        add       add task
        append    append task
        cancel    cancel words in task
        done      done task
        due       change due of task
        ls        list of tasks
        priority  change priority of task
        prune     remove task if done and today - x days >= completed x is 10 by...
        repeat    repeat add param in task for manage repeat
        rm        remove task
        txt       change txt of task and save due
        undone    undone task

Sample of Usage

::

    >> todo ls
    >> todo add test One
        [ ] 0 test One 
    >> todo add test two due:2019-11-01
        [ ] 1 test two due:2019-11-01 
    >> todo add test Three
        [ ] 2 test Three 
    >> todo ls
        [ ] 0 test One 
        [ ] 1 test two due:2019-11-01 
        [ ] 2 test Three
    >> todo rm 2
    >> todo ls
        [ ] 0 test One 
        [ ] 1 test two due:2019-11-01 
    >> todo done 1
        [X] 1 test two due:2019-11-01 
    >> todo ls
        [ ] 0 test One 
        [X] 1 test two due:2019-11-01 
    >> todo append 1 +project
        [X] 1 test two due:2019-11-01 +project 
    >> todo ls
        [ ] 0 test One 
        [X] 1 test two due:2019-11-01 +project 

Configuration
-------------

You can add file conf in application folder

Mac OS X:
~/Library/Application Support/todocli

Mac OS X (POSIX):
~/.todocli

Unix:
~/.config/todocli

Unix (POSIX):
~/.todocli

Win XP (roaming):
C:\Documents and Settings\<user>\Local Settings\Application Data\todocli

Win XP (not roaming):
C:\Documents and Settings\<user>\Application Data\todocli

Win 7 (roaming):
C:\Users\<user>\AppData\Roaming\todocli

Win 7 (not roaming):
C:\Users\<user>\AppData\Local\todocli

sample of file conf

::

    [Todo]
    Log=40 #0,10,20,30,40
    Path=todo.txt
    ColorContext=blue
    ColorDue=red
    ColorProject=yellow
    ColorNow=blue
    ColorEarlier=red
    ColorNext=black


use a specific conf

::

    >> todo -c myconf.conf ls

If you want multi todolist:

- todo
- shopping

create a specific conf: $HOME/shopping.conf with:

::

    [Todo]
    Path=shopping.txt

and add a alias

::

    alias shopping="todo -c $HOME/shopping.conf"

you can use

::

    shopping ls


If you use a webdav for save file (with user/password authentification)

::

    [Todo]
    Url=http://mywebdav/todo.txt
    User=user
    Password=password

If you want load a webdav server, you can user docker

::

    docker run -d -v <localpath>:/share --name webdav -p 80:80 fraoustin/webdav


Feature
-------

- graphic
- unittest with click