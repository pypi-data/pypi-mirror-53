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

import os
import sys
import asyncio
import argparse
import aiopg
import logging

from aqtlib.util import createLogger
from ib_insync import IB

createLogger(__name__, logging.INFO)

__all__ = ['Store']


class Store:
    """Store class initilizer

    """

    def __init__(self, name=None, symbols="symbols.csv",
                 ib_port=4001, ib_client=999, ib_server="localhost",
                 db_host="localhost", db_port="5432", db_name="aqtlib_db",
                 db_user="aqtlib_user", db_pass="aqtlib_pass", db_skip=False, orderbook=False, **kwargs):

        self.name = self.__class__.__name__
        if name is not None:
            self.name = name

        # initilize class logger
        self.log_store = logging.getLogger(__name__)

        # override args with any (non-default) command-line args
        self.args = {arg: val for arg, val in locals().items(
        ) if arg not in ('__class__', 'self', 'kwargs')}
        self.args.update(kwargs)
        self.args.update(self.load_cli_args())

        self.db_engine = None
        self.db_curr = None

    # -------------------------------------------
    def load_cli_args(self):
        parser = argparse.ArgumentParser(
            description='AQTLib Store',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

        parser.add_argument('--ib_port', default=self.args['ib_port'],
                            help='TWS/GW Port to use', required=False)
        parser.add_argument('--ib_client', default=self.args['ib_client'],
                            help='TWS/GW Client ID', required=False)
        parser.add_argument('--ib_server', default=self.args['ib_server'],
                            help='IB TWS/GW Server hostname', required=False)
        parser.add_argument('--orderbook', action='store_true',
                            help='Get Order Book (Market Depth) data',
                            required=False)
        parser.add_argument('--db_host', default=self.args['db_host'],
                            help='PostgreSQL server hostname', required=False)
        parser.add_argument('--db_port', default=self.args['db_port'],
                            help='PostgreSQL server port', required=False)
        parser.add_argument('--db_name', default=self.args['db_name'],
                            help='PostgreSQL server database', required=False)
        parser.add_argument('--db_user', default=self.args['db_user'],
                            help='PostgreSQL server username', required=False)
        parser.add_argument('--db_pass', default=self.args['db_pass'],
                            help='PostgreSQL server password', required=False)
        parser.add_argument('--db_skip', default=self.args['db_skip'],
                            required=False, help='Skip PostgreSQL logging (flag)',
                            action='store_true')

        # only return non-default cmd line args
        # (meaning only those actually given)
        cmd_args, _ = parser.parse_known_args()
        args = {arg: val for arg, val in vars(
            cmd_args).items() if val != parser.get_default(arg)}
        return args

    # -------------------------------------------
    def get_postgres_connection(self):
        if self.args['db_skip']:
            return None

        return aiopg.create_pool(
            host=self.args['db_host'],
            port=self.args['db_port'],
            user=self.args['db_user'],
            password=self.args['db_pass'],
            dbname=self.args['db_name']
        )

    # -------------------------------------------
    async def runAsync(self):
        """ Connects to PostgreSQL

        """

        # skip db connection
        if self.args['db_skip']:
            return

        # already connected?
        # if self.db_curr is not None or self.db_engine is not None:
            # return

        # connect to postgresql
        async with self.get_postgres_connection() as db:
            with (await db.cursor()) as cur:
                self.log_store.info("PostgreSQL connected...")

                # check for db schema
                await cur.execute("SELECT * FROM pg_catalog.pg_tables \
                    WHERE schemaname = 'public'")

                tables = [table[1] for table in await cur.fetchall()]

                required = ["ticks", "symbols"]
                if all(item in tables for item in required):
                    return

                # create database schema
                basedir = os.path.dirname(__file__)
                with open(os.path.join(basedir, "schema.sql")) as f:
                    schema = f.read()
                await cur.execute(schema)

                # await maybe_create_tables(engine)
                self.log_store.info("Database schema created...")

        # connect to IB
        self.connectInfo = (self.args['db_host'], self.args['db_port'], self.args['ib_client'])
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

        self.log_store.info("Connection established...")

        try:
            while True:
                pass
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)

    # -------------------------------------------
    def run(self):  # main
        """ Starts the store

        Connects to the TWS/GW, processes and logs market data,
        and broadcast it over TCP via ZeroMQ (which algo subscribe to)
        """

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.runAsync())
