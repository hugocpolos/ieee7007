#!/usr/bin/env python

import argparse
import logging
import sys

from ieee7007.instances_loader import InvalidOntologyCSVFile


def initialize_log(verbosity):
    if verbosity < 1:
        level = 99
    elif verbosity < 2:
        level = logging.INFO
    else:
        level = logging.DEBUG

    logging.basicConfig(level=level, format='[%(asctime)s] %(levelname)s - %(message)s')


def get_cli_arguments():
    parser = argparse.ArgumentParser(
        prog='7007_loader',

        description='''This program loads an IEEE 7007 ontology standard in the .owl format along
        some user-defined ontology individuals, generating a new owl ontology definition''',

        epilog='''The 7007 loader was developed by Hugo Constantinopolos.
        hugo.constantinopolos@inf.ufrgs.br''')

    parser.add_argument('ontology', choices=['evm', 'nep'])

    parser.add_argument('-f', '--individuals-input-file', action='append', nargs='+', help='''
    CSV files containing ontology individuals to be loaded.''')
    parser.add_argument('-v', '--verbose', action='count', default=0, help='display logs')
    return parser.parse_args()


def ontology_name_to_file_path(ontology_name):
    return './ontologies/{}.owl'.format(ontology_name.strip().lower())


def main():
    args = get_cli_arguments()
    initialize_log(args.verbose)

    try:
        ontology = lib.load_ontology(ontology_name_to_file_path(
            args.ontology), args.individuals_input_file, args.verbose)
    except InvalidOntologyCSVFile as err:
        logging.error(err)
        print(err, file=sys.stderr)
        return -1

    ontology.save(file='foo.owl')

    return 0


if __name__ == "__main__":
    exit(main())
