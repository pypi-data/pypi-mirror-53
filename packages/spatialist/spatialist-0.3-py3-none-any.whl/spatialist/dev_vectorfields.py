from spatialist import Raster

filename = '/home/john/PycharmProjects/spatialist/spatialist/tests/data/' \
           'S1A__IW___A_20150309T173017_VV_grd_mli_geo_norm_db.tif'

with Raster(filename) as ras:
    with ras.bbox() as vec:
        with vec['fid=0'] as sub:
            print(sub.fieldnames)
            print(sub.extent)
            print(sub.getUniqueAttributes('area'))
