"""This is pretty boiler plate right now. Later, as more command line options
are added in, this module will become more substantial."""

# --- Standard Library Imports ------------------------------------------------
# None

# --- Third Party Imports -----------------------------------------------------
import click

# --- Intra-Package Imports ---------------------------------------------------
from rtm.main import api


@click.command()
def main():
    """`rtm` on the command line will run the this function. Later, this will
    have more functionality. That's why it appear superfluous right now"""
    api.main()
