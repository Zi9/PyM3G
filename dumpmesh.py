"""M3G dumpmesh utility - dumps all meshes from a  JSR 184 3d file"""
from sys import argv
import m3g

# a = m3g.Loader(argv[1])
a = m3g.Loader("../testfiles/vrally80/car_peugeot.m3g")
meshes = []
outf = open("out.obj", "w")
for ob in a.objects:
    if isinstance(ob, m3g.Mesh):
        outf.write("o test\n")
        for i in ob.vertex_buffer.positions.vertices:
            outf.write(f"v {i[0]/100} {i[1]/100} {i[2]/100}\n")
        for i in ob.vertex_buffer.tex_coords[0].vertices:
            outf.write("vt {0} {1}\n".format(
                round(i[0]/255, 5),
                round(i[1]/255, 5)
            ))
        for i in range(0, len(ob.index_buffer[0].indices), 3):
            outf.write("f {0}/{0} {1}/{1} {2}/{2}\n".format(
                ob.index_buffer[0].indices[i]+1,
                ob.index_buffer[0].indices[i+1]+1,
                ob.index_buffer[0].indices[i+2]+1
            ))
        # meshes.append(ob)


# print(meshes[0])
# print(meshes[0].vertex_buffer.positions)
