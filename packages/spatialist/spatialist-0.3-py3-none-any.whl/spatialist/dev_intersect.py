from osgeo import ogr
from spatialist import Vector

shp1 = '/home/john/Desktop/test/subset.shp'

shp2 = '/home/john/Desktop/test/subset2.shp'

shp3 = '/home/john/Desktop/test/intersection.shp'

with Vector(shp1) as vec:
    print(vec.srs)
    print(vec.wkt)
