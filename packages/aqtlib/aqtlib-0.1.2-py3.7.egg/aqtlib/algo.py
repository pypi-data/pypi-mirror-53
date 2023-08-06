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

import logging
import argparse

from .broker import Broker
import aqtlib.util as util

util.createLogger(__name__, level=logging.INFO)

__all__ = ['Algo']


class Algo(Broker):
    def __init__(self, name=None, host="localhost", port=4001, clientId=998, **kwargs):

        # whats my name
        self.name = self.__class__.__name__

        # detect algo name
        if name is not None:
            self.name = name

        # initilize algo logger
        self.log_algo = logging.getLogger(__name__)

        # initilize strategy logger
        self._logger = logging.getLogger(__name__)

        # override args with any (non-default) command-line args
        self.args = {arg: val for arg, val in locals().items(
        ) if arg not in ('__class__', 'self', 'kwargs')}
        self.args.update(kwargs)
        self.args.update(self.load_cli_args())

        # initiate broker/order manager
        super(Algo, self).__init__(**{
            arg: val for arg, val in self.args.items() if arg in (
                'host', 'port', 'clientId')})

    # ---------------------------------------
    def load_cli_args(self):
        """
        Parse command line arguments and return only the non-default ones

        :Retruns: dict
            a dict of any non-default args passed on the command-line.
        """
        parser = argparse.ArgumentParser(
            description='AQTLib Algo',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

        parser.add_argument('--port', default=self.args["port"],
                            help='IB TWS/GW Port', type=int)
        parser.add_argument('--clientid', default=self.args["clientId"],
                            help='IB TWS/GW Client ID', type=int)
        parser.add_argument('--host', default=self.args["host"],
                            help='IB TWS/GW Server hostname')

        # only return non-default cmd line args
        # (meaning only those actually given)
        cmd_args, _ = parser.parse_known_args()
        args = {arg: val for arg, val in vars(
            cmd_args).items() if val != parser.get_default(arg)}
        return args

    # ---------------------------------------
    def run(self):
        """Starts the algo

        Connects to the Store, processes market data and passes
        tick data to the ``on_tick`` function and bar data to the
        ``on_bar`` methods.
        """
        super(Algo, self).run()
