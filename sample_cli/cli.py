import json
from cliparse import CommandArgumentParser
from cliparse.viewer.simple_table import simple_table, convert_json_to_csv

books = [
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


def initialize_db(argspec):
    pass


@simple_table
@convert_json_to_csv
def book_show(argspec):
    return json.dumps(books, indent=4, ensure_ascii=False)


def book_insert(argspec):
    book = dict(title=argspec.title,
                author=argspec.author,
                publisher=argspec.publisher)
    books.append(book)


def book_update(argspec):
    try:
        book = books[argspec.index]
    except IndexError:
        print('You typed the wrong index number. Check and try again ...')
        return

    if argspec.title:
        book['title'] = argspec.title
    if argspec.author:
        book['author'] = argspec.author
    if argspec.publisher:
        book['publisher'] = argspec.publisher
    books[argspec.index] = book
    return


def book_delete(argspec):
    index = argspec.index
    index.sort()
    index.reverse()
    try:
        for i in index:
            books.pop(i)
    except IndexError:
        print(f'Out of index. Check and try again ...')
        return


def argument_parser():
    parser = CommandArgumentParser(
        prog='',
        description='description',
        epilog='end of description', )
    sub_parser = parser.add_subparsers(dest='sub_parser')

    exit_parser = sub_parser.add_parser('exit', help='Setting Command')
    exit_parser.set_defaults(func=lambda x: exit(0))

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

    # Setting - DB Server Setting
    # ==========================================================================
    server_setting_parser = setting_init_db_parser.add_parser(
        name='server', help='Setting server')
    server_setting_parser.add_argument('-a', '--address', default='localhost',
                                       help='host address')
    server_setting_parser.add_argument('-p', '--port', type=int, default=5000,
                                       help='port')

    # ==========================================================================

    # Book Rental Manager
    # ==========================================================================
    manager_parser = sub_parser.add_parser('manager', help='Manager Command')

    manager_book_parser = manager_parser.add_subparsers(
        dest='book', help='Initialize the database')
    book_parser = manager_book_parser.add_parser('book', help='setting command')
    # viewer 옵션은 한 가지만 선택
    viewer_group = book_parser.add_mutually_exclusive_group()
    viewer_group.add_argument('-r', '--raw-data', action='store_true',
                              help='show the data as raw')
    viewer_group.add_argument('-t', '--simple-table', action='store_true',
                              help='show the data with simple table')
    book_parser.set_defaults(func=book_show)

    # Create
    book_crud_parser = book_parser.add_subparsers(dest='book_insert')

    create_parser = book_crud_parser.add_parser('insert')
    create_parser.add_argument('title', type=str)
    create_parser.add_argument('author', type=str)
    create_parser.add_argument('publisher', type=str)
    create_parser.set_defaults(func=book_insert)

    # Update
    update_parser = book_crud_parser.add_parser('update')
    update_parser.add_argument('index', type=int)
    update_parser.add_argument('-t', '--title', type=str)
    update_parser.add_argument('-a', '--author', type=str)
    update_parser.add_argument('-p', '--publisher', type=str)
    update_parser.set_defaults(func=book_update)

    delete_parser = book_crud_parser.add_parser('delete')
    delete_parser.add_argument('index', type=int, nargs='*',
                               help='index number(s) that you want to delete')
    delete_parser.set_defaults(func=book_delete)
    return parser


__all__ = ['argument_parser']

if '__main__' == __name__:
    parse = argument_parser()
    spec = parse.parse_args()
    if spec.func:
        spec.func(spec)
