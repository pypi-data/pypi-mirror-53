#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `atmodel` package."""


import unittest

from atmodel import model


@model('a')
class ModelA:
    pass


@model('a', 'b')
class ModelB:
    pass


@model('a', optional=['b'])
class ModelC:
    pass


@model('a', optional=['b', 'c'])
class ModelD:
    pass


@model('a', 'b', optional=['c', 'd'])
class ModelE:
    pass


@model(optional=['a'])
class ModelF:
    pass


@model('a', optional=[])
class ModelD:
    pass


@model('a', optional=None)
class ModelE:
    pass


@model()
class ModelF:
    pass


@model(1,2,3)
class ModelD:
    pass


class TestAtmodel(unittest.TestCase):
    """Tests for `atmodel` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""
