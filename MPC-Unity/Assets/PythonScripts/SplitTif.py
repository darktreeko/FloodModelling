from osgeo import gdal, gdalconst

filename = "TEST.tif"

driver = gdal.GetDriverByName("GTiff")

# Assumes single band (e.g. as per DEM file and loads as numpy array)
ds = gdal.Open(filename)
image = ds.ReadAsArray()


# Cut into smallest images possible, whilst ensuring side lengths of at least 1025, and ensuring equal sizes
(x,y) = image.shape
xrepeats = int(x/1025)
yrepeats = int(y/1025)
xcutlength = int(x/xrepeats)
ycutlength = int(y/yrepeats)

for i in range(xrepeats):
    for j in range(yrepeats):
        # Write to new file, for each segment
        outdata = driver.Create(f'{filename[:-4]}_{i}_{j}.tif', y, x, 1, gdalconst.GDT_UInt16)
        outdata.SetGeoTransform(ds.GetGeoTransform())
        outdata.SetProjection(ds.GetProjection())
        outdata.GetRasterBand(1).WriteArray(image[i*xcutlength:min((i+1)*xcutlength,x), j*ycutlength:min((j+1)*ycutlength,y)])
        outdata.FlushCache()

        #Convert to raw file output
        output = gdal.Translate(f'{filename[:-4]}_{i}_{j}.raw', f'{filename[:-4]}_{i}_{j}.tif', 
                                format='ENVI', outputType=gdalconst.GDT_UInt16, width = 1025, height = 1025)
        
        outdata.FlushCache()
        outdata = None

ds = None