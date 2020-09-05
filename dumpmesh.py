"""M3G dumpmesh utility - dumps all meshes from a  JSR 184 3d file"""
from sys import argv
import m3g_resolve

a = m3g_resolve.Loader(argv[1])
# a = m3g_resolve.Loader("testfiles/vrally80/car_peugeot.m3g")
outname = argv[1].split("/")[-1].replace(".m3g", ".obj")
if len(argv) == 3:
    outfolder = argv[2] + "/"
else:
    outfolder = ""
outf = open(outfolder + outname, "w")
for ob in a.objects:
    if isinstance(ob, m3g_resolve.Mesh):
        outf.write("o test\n")
        for i in ob.vertex_buffer.positions.vertices:
            outf.write(f"v {i[0]/100} {i[1]/100} {i[2]/100}\n")
        for i in ob.vertex_buffer.tex_coords[0].vertices:
            outf.write("vt {0} {1}\n".format(
                round(i[0]/128, 5) + 0.01,
                round(i[1]/128, 5) * -1 + 1
            ))
        for i in range(0, len(ob.index_buffer[0].indices), 3):
            outf.write("f {0}/{0} {1}/{1} {2}/{2}\n".format(
                ob.index_buffer[0].indices[i]+1,
                ob.index_buffer[0].indices[i+1]+1,
                ob.index_buffer[0].indices[i+2]+1
            ))
outf.close()
