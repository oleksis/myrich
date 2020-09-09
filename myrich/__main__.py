#!/usr/bin/env python
# coding: utf-8

from argparse import ArgumentParser
import os
import sys

if __package__ is None and not hasattr(sys, "frozen"):
    # direct call of __main__.py
    path = os.path.realpath(os.path.abspath(__file__))
    sys.path.insert(0, os.path.dirname(os.path.dirname(path)))

from rich.console import Console
from rich.markdown import Markdown

from . import __package_name__, __version__
from .vendor.delegator import run


console = Console()


def print_error(message):
    console.print(message, style="bold red")


def print_warning(message):
    console.print(message, style="bold yellow")


def print_output(message):
    console.print(message)


def is_command_args(cmd):
    return len(cmd.split(" ", 1)) == 2


def change_directory(path_str):
    "Change to path directory"
    cwd = None
    try:
        os.chdir(path_str)
        cwd = os.getcwd()
    except FileNotFoundError as err:
        path_str = os.getcwd()
        print_error(err)

    return cwd or path_str


def render2markdown(file_string):
    "Render file or string to Markdown"
    if os.path.isfile(file_string):
        with open(file_string) as md:
            markdown = md.read()
    else:
        markdown = file_string

    print_output(Markdown(markdown))


def run_command(commands, path_str):
    "Run commands in the path using subprocess"
    c = run(commands, cwd=path_str)
    print_output(c.out)

    if c.err:
        print_error(c.err)

    return c


# TODO: Add Columns and Logging Handler


def start_shell(cwd=None):
    "Start Shell-like"
    if not cwd:
        cwd = os.getcwd()

    while True:
        try:
            prompt = "(rich) " + cwd + "%s" % ">" if os.name == "nt" else "$ "
            command_line = input(prompt)

            if command_line and command_line.strip() == "exit":
                break

            if command_line[:2] == "cd" and is_command_args(command_line):
                cwd = change_directory(command_line[3:])
                continue
            elif command_line[:8] == "markdown" and is_command_args(command_line):
                render2markdown(command_line[9:])
                continue
            elif command_line[:6] == "myrich":
                print_warning("No action taken to avoid nested environments")
                continue

            _ = run_command(command_line, cwd)
        except KeyboardInterrupt:
            print_error("\nERROR: Interrupted by user")
            sys.exit(1)

    print_output("Bye :waving_hand:")


def main():
    "Main Entrypoint"
    retcode = 0

    # Argument Parser
    my_parser = ArgumentParser(
        prog=__package_name__,
        allow_abbrev=False,
        usage="%(prog)s [options] [commands ...]",
        description="Shell-like using Rich for render rich text content",
    )

    # Add arguments
    my_parser.version = __version__
    my_parser.add_argument(
        "-c",
        "--commands",
        action="store",
        nargs="*",
        default="",
        help="Commands string list to be executed",
    )
    my_parser.add_argument("-V", "--version", action="version")

    args = my_parser.parse_args()
    cwd = os.getcwd()

    if args.commands:
        first_command = args.commands[0]
        if len(args.commands) == 2 and first_command == "markdown":
            render2markdown(args.commands[1])
        else:
            c = run_command(args.commands, cwd)
            retcode = c.return_code
    else:
        start_shell(cwd)

    return retcode


sys.exit(main())
