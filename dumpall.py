"""M3G Dumper utility - dumps contents of JSR 184 3d files"""
from sys import argv
import timeit
import sys
sys.path.append(".")
import m3g

start = timeit.default_timer()

a = m3g.Loader(argv[1])
stop = timeit.default_timer()
index = 1
for o in a.objects:
    if not isinstance(o, str):
        print(f"{index} - {o}")
        index += 1
for o in a.objects:
    if isinstance(o, str):
        print(f"Missing reader for {o}")

a = m3g.Loader(argv[2])
stop = timeit.default_timer()
index = 1
for o in a.objects:
    if not isinstance(o, str):
        print(f"{index} - {o}")
        index += 1
for o in a.objects:
    if isinstance(o, str):
        print(f"Missing reader for {o}")
print(f"Loaded file in {round(stop-start, 5)} seconds")
