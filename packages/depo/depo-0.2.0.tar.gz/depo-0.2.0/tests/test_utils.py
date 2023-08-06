# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import depo
import json

from decimal import Decimal


class TestJSONEncoder(object):
    def test_encoding_decimal(self):
        data = {"amount": Decimal("2.27")}
        output = json.dumps(data, cls=depo.utils.JSONEncoder)
        assert output == '{"amount": "2.27"}'
