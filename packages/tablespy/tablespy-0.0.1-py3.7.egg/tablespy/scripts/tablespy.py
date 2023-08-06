#!/usr/bin/env python

import click
import os
import yaml
import sys
import random
from collections import OrderedDict

APPNAME='tablespy'
APPAUTHOR='flaxandteal'

@click.command()
@click.argument('infile')
def cli(infile):
    print(infile)
