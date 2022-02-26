#!/usr/bin/python3

import yaml
import pprint
import click
import json
from deepdiff import DeepDiff


@click.command()
@click.option('--missing', '-m', default=False, type=bool, show_default=True,
              help='If set to true, prints only missing keys. (1)')
@click.option('--ignore_order', '-ig', default=True, type=bool, show_default=True,
              help='If set to true, ignores the order of values for list items (a Set).')
@click.option('--type', '-t', default='json', type=click.Choice(['json', 'yaml']), show_default=True,
              help='The type of items you want to compare.')
@click.argument('path_to_base_file', nargs=1, required=True, type=click.Path(exists=True))
@click.argument('path_to_other_file', nargs=1, required=True, type=click.Path(exists=True))
def cli(path_to_base_file, path_to_other_file, missing, ignore_order, type):
    """Print the difference between two items (json or yaml files):\n
    1. keys that are missing from the base item comparing to the other item.\n
    2. keys that appear in the base item and not in the other item.\n
    3. difference in values for keys that appear in both items.\n
    """
    try:
        if type == 'yaml':
            baseFile = yaml_as_dict(path_to_base_file)
            otherFile = yaml_as_dict(path_to_other_file)
        else:  # JSON FILE
            baseFile = json_as_dict(path_to_base_file)
            otherFile = json_as_dict(path_to_other_file)
        diff_printer(baseFile, otherFile, missing, ignore_order)
    except Exception as e:
        click.echo("Error: " + str(e))


def yaml_as_dict(yaml_file):
    yaml_dict = {}
    with open(yaml_file, 'r') as fp:
        docs = yaml.safe_load_all(fp)
        for doc in docs:
            for key, value in doc.items():
                yaml_dict[key] = value
    return yaml_dict


def json_as_dict(json_file):
    json_dict = {}
    with open(json_file, 'r') as fp:
        json_dict = json.load(fp)
    return json_dict


def diff_printer(base_item, other_item, print_only_missing, ignore_list_order):
    ddiff = DeepDiff(base_item, other_item, ignore_order=ignore_list_order)
    print(ddiff)
    if len(ddiff) == 0:
        click.echo("Files files are equal")
        return
    if not "dictionary_item_added" in ddiff.keys():
        if print_only_missing:
            click.echo("Files are equal")
            return
    else:
        click.echo("the missing keys are:")
        printNicelyList(ddiff['dictionary_item_added'])
    if not print_only_missing:
        if "dictionary_item_removed" in ddiff.keys():
            click.echo("the extra keys are:")
            printNicelyList(ddiff['dictionary_item_removed'])
        if "values_changed" in ddiff.keys():
            click.echo("the difference in values between the files are:")
            printNicelyDict(ddiff['values_changed'])
        if "type_changes" in ddiff.keys():
            click.echo("the difference in values between the files are:")
            printNicelyDict(ddiff['type_changes'])
        if "iterable_item_added" in ddiff.keys():
            click.echo("the difference in values between the files are:")
            printNicelyDict(ddiff['iterable_item_added'])
        if "iterable_item_removed" in ddiff.keys():
            click.echo("the difference in values between the files are:")
            printNicelyDict(ddiff['iterable_item_removed'])


def printNicelyDict(a_dict):
    for key, val in a_dict.items():
        if key.startswith('root'):
            key = key[4:]
        if isinstance(val, dict):
            click.echo(pprint.pformat(key, indent=4) + ": ")
            for k, v in val.items():
                if "old" in k:
                    k = k.replace("old", "base_item")
                else:
                    k = k.replace("new", "other_item")
                click.echo("\t" + pprint.pformat(k, indent=4) + ": " + pprint.pformat(v, indent=4))
        else:
            click.echo(pprint.pformat(key, indent=4) + ": " + pprint.pformat(val, indent=4))


def printNicelyList(a_list):
    for key in a_list:
        if key.startswith('root'):
            key = key[4:]
        click.echo("\t" + pprint.pformat(key, indent=4))


if __name__ == '__main__':
    cli()
