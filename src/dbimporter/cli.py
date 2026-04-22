import click

from dbimporter.issuescheck import Issues
from dbimporter.fix_structure import Default
from dbimporter.printing import Printer
from dbimporter.check_structure import Check
from dbimporter.watcher import Watcher


@click.group(invoke_without_command=False)
@click.version_option()
def cli():
    pass

@cli.command()
@click.option('--automatic', '-x', is_flag=True, help="Whether the checker runs after the Checker has been created")
@click.option('--filename', default="src/dbimporter/data/find_unit_test.xlsx", help="path to json file to read structure")

def runcode(filename, automatic):
    Check(filename=filename, automatic_start=automatic)

@click.option('--watchpath', default=".")

@cli.command()
def watch(watchpath):
    my_watcher = Watcher(watch_path=watchpath)
    print(my_watcher.watch_path)
    my_watcher.run()