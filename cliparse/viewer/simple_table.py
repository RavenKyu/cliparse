import io
import csv
import json
import functools
from tabulate import tabulate

__all__ = ['simple_table', 'convert_json_to_csv']


def convert_json_to_csv(f):
    @functools.wraps(f)
    def func(*args, **kwargs):
        result = f(*args, **kwargs)
        if not result:
            return None

        argspec = args[0]
        if argspec.raw_data:
            print(result)
            return None
        data = json.loads(result)
        try:
            buf = io.StringIO()
            dict_writer = csv.DictWriter(buf, fieldnames=data[0].keys(),
                                         delimiter=' ',
                                         quotechar='|',
                                         quoting=csv.QUOTE_MINIMAL)
            dict_writer.writeheader()
            dict_writer.writerows(data)
            buf.seek(0)
            reader = csv.reader(buf, delimiter=' ', quotechar='|',
                                quoting=csv.QUOTE_MINIMAL)
            return list(reader)
        except IOError:
            print("I/O error")

    return func


def simple_table(f):
    @functools.wraps(f)
    def func(*args, **kwargs):
        result = f(*args, **kwargs)
        if not result:
            return
        argspec = args[0]
        print(tabulate(result, headers='firstrow', showindex="always", tablefmt="orgtbl"))

    return func
