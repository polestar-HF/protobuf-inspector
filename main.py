#!/usr/bin/env python

from sys import stdin, argv
from os.path import ismount, exists, join
from runpy import run_path
from lib.types import StandardParser

# Parse arguments
root_type = "root"
if len(argv) >= 2: root_type = argv[1]

# Load the config
config = {}
directory = "."
while not ismount(directory):
    filename = join(directory, "protobuf_config.py")
    if exists(filename):
        config = run_path(filename)
        break
    directory = join(directory, "..")

# Create and initialize parser with config
parser = StandardParser()
if "types" in config:
    for type, value in config["types"].items():
        type = unicode(type)
        assert(type not in parser.types) # FIXME: make parse_message work with non-tuples
        parser.types[type] = value
if "native_types" in config:
    for type, value in config["native_types"]:
        parser.native_types[unicode(type)] = value

# Make sure root type is defined and not compactable
if root_type not in parser.types: parser.types[root_type] = {}
parser.types[root_type]["compact"] = False

# PARSE!
print parser.safe_call(parser.match_handler("message"), stdin, root_type) + "\n"
exit(1 if len(parser.errors_produced) else 0)
