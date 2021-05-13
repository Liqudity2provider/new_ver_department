import os
import tempfile
import app
import pytest

import unittest

from app.views import view


def test_test():
    assert view.test() == "test"
