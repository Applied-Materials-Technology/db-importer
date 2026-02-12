
A Python tool to check excel files before they're are ingested into a database

## Installation:

### Virtual Environment

It is recommended to install in a virtual environment:

```
python -m venv venv
source venv/bin/activate
```

### Standard Installation

Clone to your local system and `cd` to the root directory of `db-importer`. Ensure you virtual environment is activated and run from the `db-importer` root directory:

```
pip install .
```

### Developer Installation

To create an editable installation, follow the instructions for a standard installation but run:

```
pip install -e .
```

## Getting Started

Import at the top of your code file
```
import dbimporter as dbi
```

###### Run structure check:

Note: currently, running the structure check attempts to restructure files that flag errors by default.
Turn this off by setting the no_restructure attribute to True

Run the checker with the path to the file you want to check
```
dbi.check_structure.Check(filename="path/to/file.xlsx")
```

###### Settings:
Change the console log level to remove below warning level clutter

```
dbi.check_structure.Check(filename="path/to/file.xlsx", console_loglevel = 30)
```

Toggle off colours for console logs

```
dbi.check_structure.Check(filename="path/to/file.xlsx", no_log_colour = TRUE)
```

