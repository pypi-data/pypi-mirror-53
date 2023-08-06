"""Instances of these classes contain a single row of validation information,
ready to be printed to the terminal at the conclusion of the app."""

# --- Standard Library Imports ------------------------------------------------
import abc
from typing import List
from itertools import groupby, count

# --- Third Party Imports -----------------------------------------------------
import click

# --- Intra-Package Imports ---------------------------------------------------
# None


class ValidatorOutput(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def print(self):
        return


def pretty_int_list(numbers) -> str:
    def as_range(iterable):
        """Convert list of integers to an easy-to-read string. Used to display the
    on the console the rows that failed validation."""
        list_int = list(iterable)
        if len(list_int) > 1:
            return f'{list_int[0]}-{list_int[-1]}'
        else:
            return f'{list_int[0]}'

    return ', '.join(as_range(g) for _, g in groupby(numbers, key=lambda n, c=count(): n-next(c)))


class ValidationResult(ValidatorOutput):
    """Each validation function returns an instance of this class. Calling its
    print() function prints a standardized output to the console."""
    def __init__(self, score, title, explanation=None, nonconforming_indices=None):
        self._scores_and_colors = {'Pass': 'green', 'Warning': 'yellow', 'Error': 'red'}
        self.score = score
        self._title = title
        self._explanation = explanation
        self.indices = nonconforming_indices

    @property
    def indices(self):
        return self.__indices

    @indices.setter
    def indices(self, value):
        if value is not None:
            self.__indices = list(value)
        else:
            self.__indices = []

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, value):
        if value not in self._scores_and_colors:
            raise ValueError(f'{value} is an invalid score')
        self.__score = value

    def _get_color(self):
        return self._scores_and_colors[self.score]

    @property
    def rows(self):
        first_row = 2  # this is the row # directly after the headers
        return [index + first_row for index in self.indices]

    def print(self) -> None:
        # --- Print Score in Color ------------------------------------------------
        click.secho(f"\t{self.score}", fg=self._get_color(), bold=True, nl=False)
        # --- Print Rule Title ----------------------------------------------------
        click.secho(f"\t{self._title.upper()}", bold=True, nl=False)
        # --- Print Explanation (and Rows) ----------------------------------------
        if self._explanation:

            click.secho(f' - {self._explanation}{pretty_int_list(self.rows)}', nl=False)
        click.echo()  # new line


class OutputHeader(ValidatorOutput):
    """Given a field name, print a standardized header on the console."""

    def __init__(self, header_name):
        self.field_name = header_name

    def print(self) -> None:
        sym = '+'
        box_middle = f"{sym}  {self.field_name}  {sym}"
        box_horizontal = sym * len(box_middle)
        click.echo()
        click.secho(box_horizontal, bold=True)
        click.secho(box_middle, bold=True)
        click.secho(box_horizontal, bold=True)
        click.echo()


if __name__ == '__main__':
    pass
