import sys
from distutils.core import setup

sys.argv.append('py2exe')

setup(
    options={'py2exe': {'bundle_files': 1, 'compressed': True}},
    windows=[{'script': "MissingCEOrders.py"}],
    zipfile=True,
)
