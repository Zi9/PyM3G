"""
Dumps all data from the specified m3g file when the module is called directly
"""
from sys import argv
from rich import console
from PyM3G.reader import M3GReader

c = console.Console()

m3g = M3GReader(argv[1])
for obj in m3g.objects:
    c.print(obj)
