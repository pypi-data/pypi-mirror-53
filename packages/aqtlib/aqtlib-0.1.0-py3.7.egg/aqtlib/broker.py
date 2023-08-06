#!/usr/bin/env python3
#
# MIT License
#
# Copyright (c) 2019 Kelvin Gao
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import sys
import logging

from aqtlib.util import createLogger
from ib_insync import IB

createLogger(__name__)

__all__ = ['Broker']


class Broker:
    def __init__(self, host='localhost', port=4001, clientId=666, **kwargs):

        # initilize class logger
        self.log_broker = logging.getLogger(__name__)

        # -----------------------------------
        # connect to IB
        self.connectInfo = (host, port, clientId)
        self.ib = IB()

        connection_tries = 0
        while not self.ib.isConnected():
            self.ib.connect(*self.connectInfo)
            self.ib.sleep(1)
            if not self.ib.isConnected():
                connection_tries += 1
                if connection_tries > 10:
                    self.log_broker.info(
                        "Cannot connect to Interactive Brokers...")
                    sys.exit(0)

        self.log_broker.info("Connection established...")

    def run(self):
        IB.run()
