#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
simple test queries [for DEVELOPMENT  / not part of official tests]

$ pip instal -e .
$ dimcli_quicktest 1

"""

import click 
from .. import *
from ..shortcuts import *

import requests

@click.command()
@click.argument('test_number', nargs=1)
def main(test_number=1):
    
    login()

    test_number = int(test_number)

    if test_number == 1:
        g = G
        print("*CATEGORIES*", g.categories())
        for x in g.categories():
            print("============", x, "============")
            for y in g.categories(x):
                print("...",  y)

    elif test_number == 2:
        res = dslquery("""search publications where journal.title="nature medicine" return publications[doi+FOR] limit 1000""")
        print("Query results for standard query: ")
        print(" ==> res['stats']: ", res['stats'])
        print(" ==> len(res['publications']): ", len(res['publications']))
        print(" ==> len([x for x in res.publications if 'FOR' in x]): ", len([x for x in res.publications if 'FOR' in x]))
        print("Now Normalizing the FOR key...")
        normalize_key("FOR", res.publications)
        print(" ==> len([x for x in res.publications if 'FOR' in x]): ", len([x for x in res.publications if 'FOR' in x]))       

    elif test_number == 3:
        from ..core.utils import dimensions_url
        print(dimensions_url("01", "stff",))
        print(dimensions_url("01", "publications"))


if __name__ == '__main__':
    main()



