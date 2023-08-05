"""
Runner
======

The runner is responsible for executing the parser module built by a user.

It can be configured in a number of ways:
- select the number of threaded workers, so that multiple requests can be made concurrently and the results of those requests processed in parallel.
- only process a select number of pages.
- write results to various locations and formats
"""

import importlib
import time
from datetime import datetime as dt
from types import ModuleType

from .queues import LinksQueue, ResultsQueue
from .workers import LinksWorker, ResultsWorker
from .loggers import Logger
from .parsers import Parser
from .writers import JsonWriter, Writer


class Runner(object):

    def __init__(self, parser, writer='csv', max_results=0):
        self.writer = Writer.from_string(writer)
        self.parser = Parser.from_string(parser)
        self.results = ResultsQueue(max_results=max_results)
        self.queue = LinksQueue()
        self.logger = Logger(self)
        self.link_workers = []
        self.result_workers = []

    def __str__(self):
        return f"<Runner {self.parser.module.__name__}>"

    def finished(self):
        return ResultsWorker.all_waiting(self.result_workers) and \
               LinksWorker.all_waiting(self.link_workers)

    # TODO: pull up configuration (num workers)
    def run(self):
        """
        Starts running the parser. Creates the workers and waits for them to
        finish.
        """

        self.logger.okay(f"Starting run")
        self.writer.url = f"{self.parser.module.__name__}_run_{dt.isoformat(dt.now())}"
        self.link_workers = LinksWorker.start_all(4, links_queue=self.queue, results_queue=self.results, parser=self.parser)
        self.result_workers = ResultsWorker.start_all(1, writer=self.writer, results_queue=self.results)

        while not self.finished():
            continue
        else:
            LinksWorker.stop_all(self.link_workers)
            ResultsWorker.stop_all(self.result_workers)
            self.logger.okay("Stopped all workers")
            self.logger.okay("Finished run")
