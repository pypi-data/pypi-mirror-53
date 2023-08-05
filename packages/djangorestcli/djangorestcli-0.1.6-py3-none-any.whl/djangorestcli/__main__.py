#!/usr/local/bin/python3
#!/usr/bin/python3

import argparse
import os
from djangorestcli.controllers.DjangoRestCLIController import DjangoRestCLIController

dirname = os.getcwd()
currentDirectory = os.path.dirname(os.path.abspath(__file__))


parser = argparse.ArgumentParser(
    description='Generate django rest models views and serializers automaticaly')
parser.add_argument('--make', type=str, nargs='+',
                    help='Use in this form--make app.model')

args = parser.parse_args()
controller = DjangoRestCLIController()
controller.generate(args)
