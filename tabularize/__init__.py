#!/usr/bin/env python
#
# Permission to use, copy, modify, and distribute this software and its
# documentation for any purpose and without fee is hereby granted,
# provided that the above copyright notice appear in all copies and that
# both that copyright notice and this permission notice appear in
# supporting documentation, and that the name of NIKUNJ SHARMA
# not be used in advertising or publicity pertaining to distribution
# of the software without specific, written prior permission.
# NIKUNJ SHARMA DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING
# ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL
# NIKUNJ SHARMA BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR
# ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
# IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
# OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#
# python library: Tabularize.
# https://github.com/1994nikunj/tabularize

__all__ = [
    "Tabularize",
    "PrintSampleTable"
]

__author__ = "Nikunj Sharma <1994nikunj@git.com>"
__status__ = "Development"
# The following module attributes are no longer updated.
__version__ = "1.0.0"
__date__ = "08 May 2021"

import time


# ---------------------------------------------------------------------------
#   Table Creation
# ---------------------------------------------------------------------------

class Tabularize(object):
    def __init__(self,
                 title='',
                 column_names=None,
                 left_padding: int = 1,
                 right_padding: int = 1,
                 vertical_char: str = '|',
                 horizontal_char: str = '-',
                 junction_char: str = '+',
                 space_char: str = ' '):

        # Data
        self.rows = []
        self.title = str(title)
        self.row_count = 0
        self.column_names = column_names
        self.final_printable_table_array = []
        self.column_count = len(self.column_names) or 0

        # Padding and Spacing
        self.left_padding = left_padding or 1
        self.right_padding = right_padding or 1

        # Table draw characters
        self.border = None
        self.space_char = space_char
        self.vertical_char = vertical_char
        self.junction_char = junction_char
        self.horizontal_char = horizontal_char

        if type(self.column_names) not in (list, tuple):
            raise TypeError("column_names should be of type List or Tuple")
        if type(self.left_padding) is not int:
            raise TypeError("left_padding should be of type int")
        if type(self.right_padding) is not int:
            raise TypeError("right_padding should be of type int")

    def add_row(self, row: list) -> None:
        if self.column_names and len(row) != len(self.column_names):
            raise ValueError("Row has incorrect number of values, expected: %d, actual: %d" % (
                len(self.column_names), len(row)))
        else:
            self.rows.append(list(map(str, row)))

    def generate_table(self, logger=None, _return=False, _print=True) -> str:
        returnable = ''

        self.rows.insert(0, list(map(str, self.column_names)))
        self.row_count = len(self.rows)
        max_width_arr = [max([len(self.rows[y][x]) for y in range(self.row_count)]) for x in range(self.column_count)]

        # Prepare top border
        _temp = [self.horizontal_char * (self.left_padding + y + self.right_padding) for y in max_width_arr]
        self.border = self.junction_char + self.junction_char.join(_temp) + self.junction_char

        if self.title:
            top_border = self.junction_char + self.horizontal_char * int(len(self.border) - 2) + self.junction_char
            # Topmost border (with title)
            self.final_printable_table_array.append(top_border)  # ** INSERT **
            top_border_length = len(self.border) - 4  # 4 include the 2 junction char and single left and right pad
            if len(self.title) < top_border_length:
                right_pad = top_border_length - len(self.title)
                _l = self.vertical_char + self.space_char
                _r = self.space_char + self.vertical_char
                table_title = _l + self.title + self.space_char * right_pad + _r

                self.final_printable_table_array.append(table_title)  # ** INSERT **
            else:
                raise ValueError('Title length exceeding described table, actual-length %d <= %d expected-length ' % (
                    len(self.title), top_border_length))

            self.final_printable_table_array.append(self.border)  # ** INSERT **
        else:
            # Topmost border (without title)
            self.final_printable_table_array.append(self.border)  # ** INSERT **

        for idx, x in enumerate(self.rows):
            data_row = []
            if idx == 1:
                self.final_printable_table_array.append(self.border)  # ** INSERT **
            for _id, val in enumerate(x):
                t = self.space_char * self.left_padding + val + self.space_char * int(
                    max_width_arr[_id] - len(val)) + self.space_char * self.right_padding
                data_row.append(t)
            final_row = self.vertical_char + self.vertical_char.join(data_row) + self.vertical_char
            self.final_printable_table_array.append(final_row)  # ** INSERT **

        # Insert bottom border
        self.final_printable_table_array.append(self.border)  # ** INSERT **

        # Call the final printable array function
        returnable = self.print_table(logger, _print, _return)

        return returnable

    def print_table(self, logger, print_table, return_table) -> str:
        final_print = '\n'.join([data_row for data_row in self.final_printable_table_array])
        if print_table:
            if logger:
                logger.info('\n' + final_print)
            else:
                print(final_print)

        if return_table:
            return final_print


# ---------------------------------------------------------------------------
#   Sample Date from Tabularize
# ---------------------------------------------------------------------------

class PrintSampleTable:
    def __init__(self):
        cols = ('Id', 'Name', 'Age', 'Occupation', 'DateCreated (epoch)')
        table = Tabularize(column_names=cols, right_padding=1, title="Title: Sample Table")
        table.add_row(row=[1, 'Mr. A', 27, 'IT, Software Developer', time.time()])
        table.add_row(row=[2, 'Ms. B', 23, 'Human Resource, Recruiting', time.time()])
        table.add_row(row=[3, 'Mr. C', 23, 'Banking, International Business', time.time()])
        table.add_row(row=[4, 'Mrs. D', 18, 'Student, College', time.time()])
        table.add_row(row=[5, 'Ms. E', 17, 'Student, College', time.time()])
        table.add_row(row=[6, 'Mrs. F', 12, 'Student, School', time.time()])
        table.generate_table()

# PrintSampleTable()
