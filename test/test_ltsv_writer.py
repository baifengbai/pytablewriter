# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import collections
import itertools

import pytest

import pytablewriter as ptw

from .data import (
    float_header_list,
    float_value_matrix,
    header_list,
    value_matrix,
)


Data = collections.namedtuple("Data", "header value expected")

normal_test_data_list = [
    Data(
        header=header_list,
        value=value_matrix,
        expected="""a:1\tb:123.1\tc:"a"\tdd:1\te:1
a:2\tb:2.2\tc:"bb"\tdd:2.2\te:2.2
a:3\tb:3.3\tc:"ccc"\tdd:3\te:"cccc"
"""),
    Data(
        header=header_list,
        value=[
            ["1", "", "a", "1",   None],
            [None, 2.2, None, "2.2", 2.2],
            [None, None, None, None,   None],
            [3, 3.3, "ccc", None,   "cccc"],
            [None, None, None, None,   None],
        ],
        expected="""a:1\tc:"a"\tdd:1
b:2.2\tdd:2.2\te:2.2
a:3\tb:3.3\tc:"ccc"\te:"cccc"
"""),
    Data(
        header=["a!0", "a#1", "a.2$", "a_%3", "a-&4"],
        value=[
            ["a\0b", "c   d", "e\tf", "g\nh", "i\r\nj"],
        ],
        expected="""a0:"a b"\ta1:"c   d"\ta.2:"e  f"\ta_3:"g h"\ta-4:"i j"
"""),
    Data(
        header=float_header_list,
        value=float_value_matrix,
        expected="""a:0.01\tb:0.00125\tc:0
a:1\tb:99.9\tc:0.01
a:1.2\tb:999999.123\tc:0.001
"""),
]

exception_test_data_list = [
    Data(
        header=header,
        value=value,
        expected=ptw.EmptyTableDataError)
    for header, value in itertools.product([None, [], ""], [None, [], ""])
] + [
    Data(
        header=None,
        value=value_matrix,
        expected=ptw.EmptyHeaderError),
]

table_writer_class = ptw.LtsvTableWriter


class Test_LtsvTableWriter_write_new_line(object):

    def test_normal(self, capsys):
        writer = table_writer_class()
        writer.write_null_line()

        out, _err = capsys.readouterr()
        assert out == "\n"


class Test_LtsvTableWriter_write_table(object):

    @pytest.mark.parametrize(["header", "value", "expected"], [
        [data.header, data.value, data.expected]
        for data in normal_test_data_list
    ])
    def test_normal(self, capsys, header, value, expected):
        writer = table_writer_class()
        writer.header_list = header
        writer.value_matrix = value
        writer.write_table()

        out, _err = capsys.readouterr()

        print("[expected]\n{}".format(expected))
        print("[actual]\n{}".format(out))

        assert out == expected

    @pytest.mark.parametrize(["header", "value", "expected"], [
        [data.header, data.value, data.expected]
        for data in exception_test_data_list
    ])
    def test_exception(self, header, value, expected):
        writer = table_writer_class()
        writer.header_list = header
        writer.value_matrix = value

        with pytest.raises(expected):
            writer.write_table()
