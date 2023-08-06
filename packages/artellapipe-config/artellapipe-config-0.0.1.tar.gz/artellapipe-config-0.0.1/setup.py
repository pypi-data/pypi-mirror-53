import os
import sys
from setuptools import setup

source_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'source')
if source_path not in sys.path:
    sys.path.append(source_path)

from artellapipe.config.__version__ import __version__

setup()
