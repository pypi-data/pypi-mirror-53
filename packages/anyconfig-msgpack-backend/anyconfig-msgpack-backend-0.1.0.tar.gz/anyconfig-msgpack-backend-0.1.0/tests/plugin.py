#
# Copyright (C) 2018 Satoru SATOH <satoru.satoh @ gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring,invalid-name
from __future__ import absolute_import, print_function

import os.path
import os
import unittest

import anyconfig

from tests.common import dicts_equal, CNF_0


_CURDIR = os.path.dirname(__file__)
_CNF_0 = {u'a': 0,
          u'b': u'bbb',
          u'c': 5,
          u'sect0': {u'd': [u'x', u'y', u'z']}}


class Test_90(unittest.TestCase):

    def _try_load(self, fname="0.msgpack"):
        try:
            filepath = os.path.join(_CURDIR, fname)
            cnf = anyconfig.load(filepath, ac_parser="msgpack")
        except anyconfig.UnknownFileTypeError:
            print("all types=%r" % anyconfig.list_types())
            raise

        self.assertTrue(dicts_equal(cnf, CNF_0), "%r vs. %r" % (cnf, CNF_0))

    def test_20_load(self):
        self._try_load()

# vim:sw=4:ts=4:et:
