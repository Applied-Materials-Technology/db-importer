import click
import sys

from dbimporter.issuescheck import Issues
from dbimporter.fix_structure import Default
from dbimporter.printing import Printer
from dbimporter.check_structure import Check
from dbimporter.watcher import Watcher

def modify_usage_error(main_command):

    """
        Show formatted error message
    """

    click.exceptions.UsageError.show = show

def show(self, file=None):
        
    """
        Format error message
    """

    if file is None:
        file = click._compat.get_text_stderr()

    color = None

    if self.ctx is not None:
        color = self.ctx.color

    click.utils.echo("Something went wrong...\n", file=file, color=color)   
    click.utils.echo('Error: %s\n' % self.format_message(), file=file, color=color)
    click.utils.echo("Command details: \n" + self.ctx.get_usage() + '\n', file=file, color=color)

    sys.argv = [sys.argv[0]]


@click.group(invoke_without_command=False)
@click.version_option()
def cli():
    pass

modify_usage_error(cli)

#@cli.command()
@click.option('--automatic', '-x', is_flag=True, help="Whether the checker runs after the Checker has been created")
@click.option('--filename', default="src/dbimporter/data/find_unit_test.xlsx", help="path to json file to read structure")
@cli.command()
def runcode(filename, automatic):

    my_checker = Check(filename=filename, automatic_start=automatic)
    return my_checker


@click.option('--watchpath', default=".")
@click.option('--checkopts', default=None)
@cli.command()
def watch(watchpath, checkopts):

    my_watcher = Watcher(watch_path=watchpath, checkopts=checkopts)
    print(my_watcher.watch_path)
    my_watcher.run()


@click.option('--automatic', '-x', is_flag=True, help="Whether the checker runs after the Checker has been created")
@click.option('--filename', default="src/dbimporter/data/find_unit_test.xlsx", help="path to json file to read structure")
@click.option('--watchpath', default=".", help="the path to where the file to be checked will be")
@cli.command()
def check(filename, automatic, watchpath):

    my_checker = runcode(standalone_mode = False)
    my_watcher = Watcher(watch_path=watchpath, checker=my_checker)
    my_watcher.run()

@cli.command()
@click.option('--name', default="user", help="name to be echoed back in test string")
def working(name):


    """
        Test if CLI functional. Sould return "I am working, {name}

        Parameters
        ----------
            name : str
                The word that will echo in test string. Default "user"
    """

    print(f"I am working, {name}")

