# Cliparse (CLI with ArgumentParser)

![Python package](https://github.com/RavenKyu/cliparse/workflows/Python%20package/badge.svg?branch=master) [![PyPI version](https://badge.fury.io/py/cliparse.svg)](https://badge.fury.io/py/cliparse)

__Cliparse__ is a framework to make CLI with ['Argparse'](https://docs.python.org/3/howto/argparse.html) and ['Cmd'](https://docs.python.org/3/library/cmd.html)  

[![asciicast](https://asciinema.org/a/J83RPQHIb1mAUG3TGSaplqhy4.svg)](https://asciinema.org/a/J83RPQHIb1mAUG3TGSaplqhy4)

## Concept
There are times when it is necessary that to provide a command line client like _MySQL Command line client_.
```bash
$ mysql -uroot -p

Type 'help;', or '\h' for help. Type '\C' to clean current input statement.

mysql> use test_db;
```
Some of legacy cli framework we could have chosen are not easy to extend or low productivity languages. __Cliparse__ is wrote with some of the most used modules in Python. 

`Cmd` is very common module of python for making CLI application. It provides a prompt to gets command input from user, tab auto completion, help message or usage. Actually, It's already super easy enough to make CLI applications with `Cmd`.

`Argparse` is an argument parser in command line interface. It parses options and arguments. With some short options, we can check validations which several types of arguments such as string or integer and boolean.
```python
parser = ArgumentParser(
        prog='',
        description='description',
        epilog='end of description', )
    sub_parser = parser.add_subparsers(dest='sub_parser')

    # Setting
    # ==========================================================================
    setting_parser = sub_parser.add_parser('setting', help='Setting Command')

    # Setting - DB Initializing
    # ==========================================================================
    setting_init_db_parser = setting_parser.add_subparsers(
        dest='init', help='Initialize the database')

    init_db_parser = setting_init_db_parser.add_parser(
        name='initialize-db', help='Initialize database')
    init_db_parser.add_argument('-d', '--init-db', action='store_true',
                                help='initialize database.')
    init_db_parser.add_argument('-m', '--dummy-members', action='store_true',
                                help='insert dummy members.')
    init_db_parser.add_argument('-b', '--dummy-books', action='store_true',
                                help='insert dummy books.')
    init_db_parser.add_argument('-r', '--dummy-rental', action='store_true',
                                help='insert dummy rental.')
    init_db_parser.set_defaults(func=initialize_db)
```
These awesome modules are already using for long time and easy to find how to use on web sites.

What __Cliparse__ does is to read user's argument parsers, to print the parser groups and parameters for running its function, and to make completing command line when tab. And print a result data of the function defined at the parser with some simple table viewer.

__Cliparse__ is very simple. That's all It dose.

## Features
* All command line input validation checking by `Argparse`
* Easy command line input with tab auto completion

## Installation 
```bash
$ pip install cliparse
```
or
```bash
$ python setup.py install
```

### Running 
```bash
$ python -m cliparse ./sample_cli/cli.py 
```

### Running with docker
If you use docker, you can try it like below. 
#### Build
```bash
$ docker build -t cliparse:latest .
``` 
or
```bash
$ docker-compose build
```
#### Running
**the volume option for mounting host directory where the sample cli is.** 
```bash
$ docker run -it -v $(pwd):/root --rm cliparse sample_cli/cli.py 
```
or
```bash
$ docker-compose run -v $(pwd):/root --rm cliparse sample_cli/cli.py
```

### sample_cli/cli.py
This sample cli file is also able to run without __Cliparse__. 
```bash
python sample_cli/cli.py -h
```
---
## Sample
There is a simple sample cli which is able to try basic CRUD. It is in the directory named `sample_cli/cli.py`. Please run command below and try to edit as you want.
### Things you can do
#### Help
All most each menu can show its help message or usage. 
```bash
# Help
(Cmd) help

Documented commands (type help <topic>):
========================================
help  manager  setting
```
```bash
(Cmd) manager -h
usage:  manager [-h] {book} ...

positional arguments:
  {book}      Initialize the database
    book      setting command

optional arguments:
  -h, --help  show this help message and exit
```
```bash
(Cmd) manager book -h
usage: manager book [-h] [-r | -t] {insert,update,delete} ...

positional arguments:
  {insert,update,delete}

optional arguments:
  -h, --help            show this help message and exit
  -r, --raw-data        show the data as raw
  -t, --simple-table    show the data with simple table
```

#### Tapping tab key 
Please, try to tap tab key for completing command line input automatically. Also it shows you command list you can use next. 

#### Choosing presentation style 
````bash
# show --raw-data
(Cmd) manager book --raw-data
[
    {
        "author": "John Doe",
        "title": "How to learn speaking English",
        "publisher": "Magic House"
    },
    {
        "author": "George Orwell",
        "title": "1984",
        "publisher": "Motihari"
    }
]

# show data with simple table
(Cmd) manager book --simple-table
|    | author        | title                         | publisher   |
|----+---------------+-------------------------------+-------------|
|  0 | John Doe      | How to learn speaking English | Magic House |
|  1 | George Orwell | 1984                          | Motihari    |
````

## Contributes
### Running as develop mode
It doesn't need to build the docker image every time when ever source code edited. 
```bash
docker-compose -f docker-compose.dev.yml run --rm cliparse
```

