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
    my_checker = Check(filename=filename, automatic_start=automatic)
    return my_checker

@click.option('--watchpath', default=".")
@click.option('--checker', default=None)

@cli.command()
def watch(watchpath, checker):
    my_watcher = Watcher(watch_path=watchpath)
    print(my_watcher.watch_path)
    my_watcher.run()

@cli.command()
@click.option('--automatic', '-x', is_flag=True, help="Whether the checker runs after the Checker has been created")
@click.option('--filename', default="src/dbimporter/data/find_unit_test.xlsx", help="path to json file to read structure")
@click.option('--watchpath', default=".", help="the path to where the file to be checked will be")
#@click.option('--checker', default=None, help="the checker used to carry out checks")
def check(filename, automatic, watchpath):
    #my_checker = Check(filename=filename, automatic_start=automatic)
    #my_checker = hello(standalone_mode=False))
    my_checker = runcode(standalone_mode = False)
    my_watcher = Watcher(watch_path=watchpath, checker=my_checker)
    my_watcher.run()
