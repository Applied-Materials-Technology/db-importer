import click

def start():

    print("Hello world")

def some_function(folder, add, edit):
    return None

@click.group(invoke_without_command=False)
@click.version_option()
def cli():
    pass


@cli.command()
@click.option(
    "--folder",
    "-f",
    default="",
    help="Specify a folder to filter the notes (leave empty to get all).",
)
@click.option(
    "--add",
    "-a",
    is_flag=True,
    help="Add a note to the specified folder. Specify a folder using the --folder flag.",
)
@click.option(
    "--edit",
    "-e",
    is_flag=True,
    help="Edit a note in the specified folder. Specify a folder using the --folder flag.",
)

def notes(
    folder, add, edit,):

    some_function(folder, edit, add)

    if edit:
        print("I've edit")
        return None
    if add:
        print("I've add")
        return None
