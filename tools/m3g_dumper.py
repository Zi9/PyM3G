"""M3G Dumper utility - dumps contents of JSR 184 3d files"""
from sys import argv
import timeit
import m3g

start = timeit.default_timer()

a = m3g.Loader(argv[1])
stop = timeit.default_timer()

for o in a.objects:
    if not isinstance(o, str):
        print(f"{o}")
for o in a.objects:
    if isinstance(o, str):
        print(f"Missing reader for {o}")

print(f"Loaded file in {round(stop-start, 5)} seconds")
