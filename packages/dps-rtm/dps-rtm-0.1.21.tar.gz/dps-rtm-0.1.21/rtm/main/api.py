"""The main() function here defines the structure of the RTM Validation
process. It calls the main steps in order and handles exceptions directly
related to validation errors (e.g. missing columns)"""

# --- Standard Library Imports ------------------------------------------------
# None

# --- Third Party Imports -----------------------------------------------------
import click

# --- Intra-Package Imports ---------------------------------------------------
from rtm.main.excel import get_rtm_path
from rtm.main.exceptions import RTMValidatorError
from rtm.containers.fields import Fields
import rtm.containers.worksheet_columns as wc
import rtm.containers.work_items as wi
import rtm.main.context_managers as context


def main(path=None):
    """This is the main function."""


    click.clear()
    click.echo(
        "\nWelcome to the DePuy Synthes Requirements Trace Matrix (RTM) Validator."
        "\nPlease select an RTM excel file you wish to validate."
    )


    try:
        if not path:
            path = get_rtm_path()
        with context.path.set(path):
            worksheet_columns = wc.WorksheetColumns("Procedure Based Requirements")
        with context.worksheet_columns.set(worksheet_columns):
            fields = Fields()
        with context.fields.set(fields):
            work_items = wi.WorkItems()
        with context.fields.set(fields), context.work_items.set(work_items):
            fields.validate()
            fields.print()
    except RTMValidatorError as e:
        click.echo(e)

    click.echo(
        "\nThank you for using the RTM Validator."
        "\nIf you have questions or suggestions, please contact a Roebling team member.\n"
    )


if __name__ == "__main__":
    main()
