# from osgeo import ogr
# from spatialist import Vector, crsConvert
#
# # geom = ogr.Geometry(ogr.wkbMultiPoint)
#
# point1 = ogr.Geometry(ogr.wkbPoint)
# point1.AddPoint(11.4, 50.1)
#
# # point2 = ogr.Geometry(ogr.wkbPoint)
# # point2.AddPoint(12.4, 51.1)
#
# point = None
#
# crs = crsConvert(4326, 'osr')
#
# with Vector(driver='Memory') as vec:
#     vec.addlayer('test', crs, point1.GetGeometryType())
#     # vec.addfield('id', type=ogr.OFTInteger)
#
#     feature1 = ogr.Feature(vec.layerdef)
#     feature1.SetGeometry(point1)
#
#     feature2 = ogr.Feature(vec.layerdef)
#     feature2.SetGeometry(point2)
#     # for key, value in fields.items():
#     #     feature.SetField(key, value)
#     vec.layer.CreateFeature(feature1)
#     vec.layer.CreateFeature(feature2)
#
#     print(vec.layer.GetFeature(2))
#
#     vec.write('/home/john/Desktop/testfile.shp')
#####################################################################
# from spatialist import bbox
#
# coords = {'xmin': 50, 'xmax': 51, 'ymin': 11, 'ymax': 12}
#
# bbox(coords, crs=4326, outname='/home/john/Desktop/bbox_new.shp')
#####################################################################
from osgeo import osr, ogr
from spatialist import crsConvert





x, y = coordinate_reproject(11, 50, 4326, 32631)

print(x + y)
