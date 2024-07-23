import os, sys

script_dir = os.path.dirname(os.path.abspath(__file__))
print(script_dir)
sys.path.append(script_dir)

from .BivittatusDB import *