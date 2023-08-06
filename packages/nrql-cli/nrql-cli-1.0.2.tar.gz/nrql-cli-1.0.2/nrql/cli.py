#!/usr/bin/python3
"""
nrql-cli - An interactive command line interface for querying NRQL data.
"""

from __future__ import unicode_literals

import json
import os
import platform
import sys
import time
from argparse import ArgumentParser

import colorful
import requests
from halo import Halo
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import Style
from pygments import highlight, lexers, formatters
from pygments.lexers.sql import SqlLexer

WORDS = "/tmp/words.json"
INSIGHTS_URL = "https://insights-api.newrelic.com/v1/accounts/%s/query"
INSIGHTS_EU_REGION_URL = "https://insights-api.eu.newrelic.com/v1/accounts/%s/query"


def creation_date(path_to_file):
    """
    Get the creation date of the file.
    :param path_to_file: str
    :return: str
    """
    if platform.system() == "Windows":
        return os.path.getctime(path_to_file)
    stat = os.stat(path_to_file)
    try:
        return stat.st_birthtime
    except AttributeError:
        return stat.st_mtime


def generate_word_list():
    """
    Generate word list.
    :return:
    """
    event_types_query = "show event types since 1 week ago"
    keyset_query = "select keyset() from %s since 1 week ago"
    with Halo(text="Loading...", spinner="dots"):
        reserved_words = [
            "ago",
            "and",
            "as",
            "auto",
            "begin",
            "begintime",
            "compare",
            "day",
            "days",
            "end",
            "endtime",
            "explain",
            "facet",
            "from",
            "hour",
            "hours",
            "in",
            "is",
            "like",
            "limit",
            "minute",
            "minutes",
            "month",
            "months",
            "not",
            "null",
            "offset",
            "or",
            "second",
            "seconds",
            "select",
            "since",
            "timeseries",
            "until",
            "week",
            "weeks",
            "where",
            "with"
        ]
        nrql = NRQL()
        events = nrql.query(event_types_query)
        events = events["results"][0]["eventTypes"]
        keysets = nrql.query(keyset_query % ", ".join(event for event in events))
        words = list(
            set(reserved_words + events + keysets["results"][0]["allKeys"])
        )
    return words


def load_or_generate():
    """
    Check if the word file exists.
    If it does read and decode JSON otherwise generate the word list and write to /tmp/words.json
    :return:
    """
    if not os.path.isfile(WORDS):
        with open(WORDS, "w") as outfile:
            word_list = generate_word_list()
            json.dump({"words": word_list}, outfile)
            return word_list
    filename = creation_date(WORDS)
    timestamp_now = time.time()
    difference = abs(filename - timestamp_now) / 60 / 60 / 24
    if difference > 7:
        word_list = generate_word_list()
        with open(WORDS, "w") as outfile:
            json.dump({"words": word_list}, outfile)
        return word_list

    with open(WORDS) as filename:
        word_list = json.load(filename)
        return word_list["words"]


def arg_parser():
    """
    Argument parser.
    :return: arr
    """
    parser = ArgumentParser(prog="nrql_cli")
    parser.add_argument(
        "--region",
        "--r",
        default="US",
        choices=["EU", "US"],
        help="Set your region (EU or US) By default the region is set to US.",
    )
    parser.add_argument("--env", "--e", help="Environment handler.")
    parser.add_argument(
        "--verbose",
        "--v",
        dest="verbose",
        action="store_true",
        default=False,
        help="Output the whole response.",
    )
    args = parser.parse_args()
    return args


class NRQL:
    """
    NRQL API.
    """

    def __init__(self, api_key=None, account_id=None):
        """
        :param api_key: The Insights query API key.
        :param account_id: The New Relic account id.
        """
        self.api_key = api_key
        self.account_id = account_id
        self._url = INSIGHTS_URL
        self._eu_url = INSIGHTS_EU_REGION_URL
        self._region = "US"
        self._verbose = False
        self._environment = None

    @property
    def api_key(self) -> str:
        """
        The Insights query API key.
        :return: str
        """
        return self._api_key

    @api_key.setter
    def api_key(self, api_key: str):
        """
        Set the Insights query API key.
        :param api_key: atr
        :return: str
        """
        self._api_key = api_key

    @property
    def account_id(self) -> str:
        """
        Set the New Relic account id.
        :return: str
        """
        return self._account_id

    @account_id.setter
    def account_id(self, account_id: str):
        """
        The New Relic account id.
        :param account_id:
        :return: str
        """
        self._account_id = account_id

    @property
    def region(self) -> str:
        """
        The account region.
        :return: str
        """
        return self._region

    @region.setter
    def region(self, region: str):
        """
        Set the account region (EU or US). By default the region is set to US.
        :param region: str
        :return: str
        """
        self._region = region

    @property
    def verbose(self) -> bool:
        """
        If True output the entire JSON response.
        :return: bool
        """
        return self._verbose

    @verbose.setter
    def verbose(self, verbose: bool):
        """
        Set to True output the entire JSON response.
        :param verbose:
        :return:
        """
        self._verbose = verbose

    @property
    def environment(self) -> str:
        """
        # The development environment.
        :return: str
        """
        return self._environment

    @environment.setter
    def environment(self, environment: str):
        """
        # Set the environment.
        :param environment:
        :return:
        """
        self._environment = environment

    @staticmethod
    def _print_messages(response):
        if "metadata" in response and "messages" in response["metadata"]:
            for message in response["metadata"]["messages"]:
                print(colorful.bold(message))

    def _multiple_account_handler(self):
        if self.environment is None:
            nr_api_key = os.environ.get("NR_API_KEY")
            nr_account_id = os.environ.get("NR_ACCOUNT_ID")
        else:
            nr_api_key = os.environ.get("NR_API_KEY_%s" % self.environment.upper())
            nr_account_id = os.environ.get(
                "NR_ACCOUNT_ID_%s" % self.environment.upper()
            )
        return nr_api_key, nr_account_id

    def _make_request(self, query_stmt):
        payload = {"nrql": query_stmt}
        req = requests.get(
            self._url % self.account_id,
            headers={"X-Query-Key": self.api_key},
            params=payload,
        )
        if self.verbose:
            print(colorful.bold("Request URL: %s" % req.url))
            print(colorful.bold("Status Code: %s" % req.status_code))
        response = req.json()
        self._print_messages(response)
        if not self.verbose:
            response.pop("metadata", None)
            response.pop("performanceStats", None)

        return response

    def query(self, stmt):
        """
        Parse the query.
        :param stmt: str
        :return: str
        """
        nr_api_key, nr_account_id = self._multiple_account_handler()
        if not self.api_key or not self.account_id:
            if nr_api_key and nr_account_id:
                self._api_key = nr_api_key
                self._account_id = nr_account_id
            else:
                raise Exception("An api key and account id is required.")

        if not self.region == "US":
            self._url = self._eu_url

        resp = self._make_request(stmt)
        return resp


def main():
    """
    usage: nrql_cli [-h] [--region {EU,US}] [--env ENV] [--verbose]

    optional arguments:
      -h, --help            show this help message and exit
      --region {EU,US}, --r {EU,US}
                            Pass this flag to set your region (EU or US) By
                            default the region is set to US.
      --env ENV, --e ENV    Environment handler.
      --verbose, --v        Pass this flag if you want the whole response.
        :return:
    """
    style = Style.from_dict(
        {
            "completion-menu.completion": "bg:#008888 #ffffff",
            "completion-menu.completion.current": "bg:#00aaaa #000000",
            "scrollbar.background": "bg:#88aaaa",
            "scrollbar.button": "bg:#222222",
        }
    )
    args = arg_parser()
    nrql = NRQL()
    nrql.verbose = args.verbose
    nrql.region = args.region
    nrql_completer = WordCompleter(load_or_generate(), ignore_case=True)
    session = PromptSession(
        lexer=PygmentsLexer(SqlLexer), completer=nrql_completer, style=style
    )
    print("Welcome to your data, let's get querying...")
    while True:
        try:
            text = session.prompt("> ")
        except KeyboardInterrupt:
            continue
        except EOFError:
            break
        else:
            if not (text and text.strip()):
                continue
            if text == "quit()":
                sys.exit(0)
            spinner = Halo(spinner="dots")
            spinner.start()
            req = nrql.query(text)
            spinner.stop()
            formatted_json = json.dumps(req, sort_keys=True, indent=4)
            print(
                highlight(
                    str(formatted_json).encode("utf-8"),
                    lexers.JsonLexer(),
                    formatters.TerminalFormatter(),
                )
            )


if __name__ == "__main__":
    main()
