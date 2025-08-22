# PyM3G

A small library to parse JSR 184 format .m3g files. These files are mostly used in J2ME mobile games.


## This repo is archived. For the latest code check out [this fork](https://github.com/BaalNetbek/PyM3G/)


### Example usage
---
Included is a small demo utility to print out all the properties of a .m3g file when the module is called directly:

```python
$ python -m PyM3G testfiles/vrally/car_subaru.m3g
(0) Header:
        Version: 1.0
        Has external references: False
        Total file size: 6277
        Approximate content size: 6277
        Authoring field text: ''

(1) VertexArray:
        Component Size: 2
        Component Count: 3
        Encoding: 0
        Vertex Count: 339
        Vertices: Array of 339 items

(2) VertexArray:
        Component Size: 1
        Component Count: 3
        Encoding: 0
        Vertex Count: 339
        Vertices: Array of 339 items

(3) VertexArray:
        Component Size: 1
........
```
