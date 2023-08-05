"""
mutalyzer_hgvs_parser: Parser for HGVS variant descriptions.


Copyright (c) 2019 Leiden University Medical Center <humgen@lumc.nl>
Copyright (c) 2019 Mihai Lefter <m.lefter@lumc.nl>


...
"""
from .mutalyzer_hgvs_parser import parse_description,\
    parse_description_to_model

__version_info__ = ('0', '0', '1')


__version__ = '.'.join(__version_info__)
__author__ = 'LUMC, Mihai Lefter, Jeroen Laros, Martijn Vermaat'
__contact__ = 'M.Lefter@lumc.nl'
__homepage__ = 'https://github.com/mutalyzer/hgvs-parser'

usage = __doc__.split("\n\n\n")


def doc_split(func):
    return func.__doc__.split("\n\n")[0]


def version(name):
    return "%s version %s\n\nAuthor   : %s <%s>\nHomepage : %s" % \
           (name, __version__, __author__, __contact__, __homepage__)
