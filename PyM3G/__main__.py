"""
Dumps all data from the specified m3g file when the module is called directly
"""
from sys import argv
from .M3GReader import M3GReader
from rich import console

c = console.Console()

m3g = M3GReader(argv[1])
for obj in m3g.objects:
    c.print(obj)
