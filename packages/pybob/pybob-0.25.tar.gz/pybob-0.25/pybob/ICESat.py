"""
pybob.ICESat provides an interface to extracted ICESat(-1) data stored in HDF5 format. Pre-extracted ICESat tracks for
    each of the RGI subregions can be found `here <http://tinyurl.com/UiOICESat>`_.
"""
from __future__ import print_function
#from future_builtins import zip
from collections import OrderedDict
import os
import h5py
import numpy as np
import pandas as pd
import pyproj
import fiona
import subprocess
from osgeo import ogr, osr
from pybob.GeoImg import GeoImg
import matplotlib.pyplot as plt
from shapely.geometry import Point, mapping
#import numpy as np


def get_file_info(in_filestring):
    in_filename = os.path.basename(in_filestring)
    in_dir = os.path.dirname(in_filestring)
    if in_dir == '':
        in_dir = '.'
    return in_filename, in_dir


def find_keyname(keys, subkey, mode='first'):
    out_keys = [k for k in keys if subkey in k]
    if mode == 'first':
        return out_keys[0]
    elif mode == 'last':
        return out_keys[-1]
    else:
        return out_keys


def extract_ICESat(in_filename,workdir=None,outfile=None):
    """
    Extract ICESat data given the extent of a GeoImg.

    **Note - currently not supported outside of UiO working environment.**

    :param in_filename: Filename (optionally with path) of DEM to be opened using GeoImg.
    :param workdir: Directory where in_filename is located. If not given, the directory
        will be determined from the input filename.
    :param outfile: name of the output file [default='ICESat_DEM.h5']

    :type in_filename: str
    :type workdir: str
    :type outfile: str
    """

    def getExtent(in_filename):
    #This function uses GeoImg.find_valid_bbox to get the extent, then projects 
    #extent into the same reference system as in_filename
    #in_filename - input filename (string). should be a geotiff
        myDEM = GeoImg(in_filename)
        mybbox = myDEM.find_valid_bbox()
        
        # Setup the source projection - you can also import from epsg, proj4...
        source = osr.SpatialReference()
        source.ImportFromEPSG(myDEM.epsg)
    
        # The target projection
        target = osr.SpatialReference()
        target.ImportFromEPSG(4326)
    
        # Create the transform - this can be used repeatedly
        transform = osr.CoordinateTransformation(source, target)
    
        # Transform the point. You can also create an ogr geometry and use the more generic `point.Transform()`
        J1 = transform.TransformPoint(mybbox[0], mybbox[2])
        J2 = transform.TransformPoint(mybbox[1], mybbox[3])
        
        minLat = J1[1]
        maxLat = J2[1]
        
        minLon = J1[0]
        maxLon = J2[0]
        
    #    if minLon<0:
    #        minLon = 360 + minLon
    #    if maxLon<0:
    #        maxLon = 360 + maxLon
    
        return minLat, maxLat, minLon, maxLon
        
    #workdir = os.path.abspath(workdir)
    minLat, maxLat, minLon, maxLon = getExtent(in_filename)    
    
    # Hard coded name of the input configuration file for ICESat extraction. Here we will 
    # read it in, modify it using the extent of a GeoImg
    filename="/net/lagringshotell/uio/lagringshotell/geofag/icemass/icemass-data/ICESatData/ICESat_archive/Programs/user_input_running.txt"
    
    # Check for the working directory, and set if None
    if workdir is None: 
        workdir= os.path.abspath('./')
    tfilename = workdir + os.path.sep + "ICESat_input.txt"
    # Read in the input_file for icesat extraction
    with open(filename) as f:
        lines = f.readlines()
        #print lines

    # Set the output file 
    if outfile is None: 
        outfile='ICESat_DEM.h5'
    # replace lines
    strout = str(minLat) + "\t" + str(maxLat) + "\t" + str(minLon) + "\t" + str(maxLon)
    lines[10] = strout + "\n"
    lines[12] = outfile + "\n"    
    
    # write output configuration file
    with open(tfilename, 'w') as f:
        for item in lines:
            f.write(str(item))
    
    # Here run bash command to the ICESat extraction routine using our newly created config file
    bshcmd = "module load ICESat; importICESat -np 20 -in " + str(tfilename) + " > ICESat_import_LOG.txt"
    subprocess.call(bshcmd,stdout=subprocess.PIPE, shell=True)
    
    pass

class ICESat(object):
    """Create an ICESat dataset from an HDF5 file containing ICESat data."""

    def __init__(self, in_filename, in_dir=None, cols=['lat', 'lon', 'd_elev', 'd_UTCTime'], ellipse_hts=True):
        """
        :param in_filename: Filename (optionally with path) of HDF5 file to be read in.
        :param in_dir: Directory where in_filename is located. If not given, the directory
            will be determined from the input filename.
        :param cols: Columns to read in and set as attributes in the ICESat object.
            Default values are ['lat', 'lon', 'd_elev', 'd_UTCTime'], and will
            be added if not specified.
        :param ellipse_hts: Convert elevations to ellipsoid heights. Default is True.
        :type in_filename: str
        :type in_dir: str
        :type cols: array-like
        :type ellipse_hts: bool

        The following example:

        >>> ICESat('donjek_icesat.h5', ellipse_hts=True)

        will return an ICESat object with lat, lon, elevation, and UTCTime attributes, with elevations given as height
        above WGS84 ellipsoid.
        """
        if in_dir is None:
            in_filename, in_dir = get_file_info(in_filename)
        self.filename = in_filename
        self.in_dir_path = in_dir
        self.in_dir_abs_path = os.path.abspath(in_dir)

        h5f = h5py.File(os.path.join(self.in_dir_path, self.filename),'r')
        h5data = h5f['ICESatData']  # if data come from Anne's ICESat scripts, should be the only data group
        data_names = h5data.attrs.keys()
        # make sure that our default attributes are included.
        for c in ['lat', 'lon', 'd_elev', 'd_UTCTime']:
            if c not in cols:
                cols.append(c)
                
        for c in cols:
            key = find_keyname(data_names, c, 'first')
            ind = h5data.attrs.get(key)[0]
            # set the attribute, removing d_ from the attribute name if it exists
            setattr(self, c.split('d_', 1)[-1], h5data[ind, :])
            if c == 'lon':
                # return longitudes ranging from -180 to 180 (rather than 0 to 360)
                self.lon[self.lon > 180] = self.lon[self.lon > 180] - 360

        self.data_names = data_names
        self.column_names = cols
        self.h5data = h5data
        self.ellipse_hts = False
        self.proj = pyproj.Proj(init='epsg:4326')
        self.x = self.lon
        self.y = self.lat
        self.xy = list(zip(self.x, self.y))

        if ellipse_hts:
            self.to_ellipse()

    def to_ellipse(self):
        """
        Convert ICESat elevations to ellipsoid heights, based on the data stored in the HDF5 file.
        """
        # fgdh = find_keyname(self.data_names, 'd_gdHt')
        kde = find_keyname(self.data_names, 'd_deltaEllip', 'first')
        ide = self.h5data.attrs.get(kde)[0]
        de = self.h5data[ide, :]
        self.ellipse_hts = True
        self.elev = self.elev + de

    def from_ellipse(self):
        """
        Convert ICESat elevations from ellipsoid heights, based on the data stored in the HDF5 file.
        """
        kde = find_keyname(self.data_names, 'd_deltaEllip', 'first')
        ide = self.h5data.attrs.get(kde)[0]
        de = self.h5data[ide, :]
        self.ellipse_hts = False
        self.elev = self.elev - de

    def to_shp(self, out_filename, driver='ESRI Shapefile', epsg=4326):
        """
        Write ICESat data to shapefile.

        :param out_filename: Filename (optionally with path) of file to read out.
        :param driver: Name of driver fiona should use to create the outpufile. Default is 'ESRI Shapefile'.
        :param epsg: EPSG code to project data to. Default is 4326, WGS84 Lat/Lon.
        :type out_filename: str
        :type driver: str
        :type epsg: int

        Example:

        >>> donjek_icesat.to_shp('donjek_icesat.shp', epsg=3338)

        will write donjek_icesat to a shapefile in Alaska Albers projection (EPSG:3338)
        """
        # skip the lat, lon columns in the h5data
        # get the columns we're writing out
        props = []
        prop_inds = []
        data_names = [d.split('/')[-1] for d in self.data_names]

        for i, d in enumerate(data_names):
            props.append([d.rsplit(str(i), 1)[0], 'float'])
            prop_inds.append(i)
        lat_key = find_keyname(data_names, 'lat', 'first')
        lat_ind = self.h5data.attrs.get(lat_key)[0]
        lon_key = find_keyname(data_names, 'lon', 'first')
        lon_ind = self.h5data.attrs.get(lon_key)[0]
        prop_inds.remove(lat_ind)
        prop_inds.remove(lon_ind)

        props = OrderedDict(props)
        del props['d_lat'], props['d_lon']
                
        schema = {'properties': props, 'geometry': 'Point'}

        outfile = fiona.open(out_filename, 'w', crs=fiona.crs.from_epsg(epsg), driver=driver, schema=schema)
        lat = self.lat
        lon = self.lon
        
        if epsg != 4326:
            dest_proj = pyproj.Proj(init='epsg:{}'.format(epsg))
            x, y = pyproj.transform(pyproj.Proj(init='epsg:4326'), dest_proj, lon, lat)
            pts = zip(x, y)
        else:
            pts = zip(lat, lon)

        for i, pt in enumerate(pts):
            this_data = self.h5data[prop_inds, i]
            out_data = OrderedDict(zip(props.keys(), this_data))
            point = Point(pt)
            outfile.write({'properties': out_data, 'geometry': mapping(point)})

        outfile.close()
        
    def to_csv(self, out_filename):
        """
        Write ICESat data to csv format using pandas.
        
        :param out_filename: Filename (optionally with path) of file to read out.
        :type out_filename: str
        """
        darr = np.transpose(np.array(self.h5data))
        data_names = [d.split('/')[-1] for d in self.data_names]
        for i, d in enumerate(data_names):
            data_names[i] = d.rsplit(str(i), 1)[0]
        df = pd.DataFrame(darr, columns=data_names)
        df['x'] = self.x
        df['y'] = self.y
        df['z'] = self.elev
    
        col_names = ['x', 'y', 'z']
        col_names.extend(data_names)
        df = df[col_names]
        del df['d_elev']
        del df['d_lat']
        del df['d_lon']
    
        df.to_csv(out_filename, index=False)
        
    def clean(self, el_limit=-500):
        """
        Remove all elevation points below a given elevation.

        :param el_limit: minimum elevation to accept
        :type el_limit: float
        """
        mykeep = self.elev > el_limit
        self.x = self.x[mykeep]
        self.y = self.y[mykeep]
        self.elev = self.elev[mykeep]
        self.xy = list(zip(self.x,self.y))

    def mask(self, mask, mask_value=True, drop=False):
        """
        Mask values

        :param mask: Array of same size as self.img corresponding to values that should be masked.
        :param mask_value: Value within mask to mask. If True, masks image where mask is True. If numeric, masks image
            where mask == mask_value.
        :param drop: remove values from dataset (True), or mask using numpy.masked_array (False). Default is False.
        :type mask: array-like
        :type mask_value: bool or numeric
        :type drop: bool
        """
        if mask_value is not bool:
            mask = mask == mask_value

        if not drop:
            self.x = np.ma.masked_where(mask, self.x)
            self.y = np.ma.masked_where(mask, self.y)

            for c in self.column_names:
                this_attr = getattr(self, c.split('d_', 1)[-1])
                masked_attr = np.ma.masked_where(mask, this_attr)
                setattr(self, c.split('d_', 1)[-1], masked_attr)
        else:
            self.x = self.x[mask]
            self.y = self.y[mask]
            for c in self.column_names:
                this_attr = getattr(self, c.split('d_', 1)[-1])
                masked_attr = this_attr[mask]
                setattr(self, c.split('d_', 1)[-1], masked_attr)

        self.xy = list(zip(self.x, self.y))

    def unmask(self):
        """
        Remove a mask if it has been applied.
        **TODO: Not implemented yet!**

        :return:
        """
        pass

    def clip(self, bounds):
        """
        Remove ICEsat data that falls outside of a given bounding box.

        :param bounds: bounding box to clip to, given as xmin, xmax, ymin, ymax
        :type bounds: array-like
        """
        xmin, xmax, ymin, ymax = bounds
        mykeep_x = np.logical_and(self.x > xmin, self.x < xmax)
        mykeep_y = np.logical_and(self.y > ymin, self.y < ymax)
        mykeep = np.logical_and(mykeep_x, mykeep_y)
        
        self.x=self.x[mykeep]
        self.y=self.y[mykeep]
        self.elev=self.elev[mykeep]
        self.xy = list(zip(self.x,self.y))
        pass
    
    def get_bounds(self, geo=False):
        """
        Return bounding coordinates of the dataset.

        :param geo: Return geographic (lat/lon) coordinates (default is False)
        :type geo: bool

        :returns bounds: xmin, xmax, ymin, ymax values of dataset.

        Example:
        >>> xmin, xmax, ymin, ymax = my_icesat.get_bounds()
        """
        if not geo:
            return self.x.min(), self.x.max(), self.y.min(), self.y.max()
        else:
            return self.lon.min(), self.lon.max(), self.lat.min(), self.lat.max()

    def project(self, dest_proj):
        """
        Project the ICESat dataset to a given coordinate system, using pyproj.transform.
        ICESat.project does not overwrite the lat/lon coordinates, so calling
        ICESat.project will only update self.x,self.y for the dataset, self.xy, and self.proj.

        :param dest_proj: Coordinate system to project the dataset into. If dest_proj is a string,
            ICESat.project() will create a pyproj.Proj instance with it.
        :type dest_proj: str or pyproj.Proj

        Example:
        Project icesat_data to Alaska Albers (NAD83) using epsg code:

        >>> icesat_data.project('epsg:3338')
        """
        if isinstance(dest_proj, str):
            dest_proj = pyproj.Proj(init=dest_proj)
        wgs84 = pyproj.Proj(init='epsg:4326')
        self.x, self.y = pyproj.transform(wgs84, dest_proj, self.lon, self.lat)
        self.xy = list(zip(self.x, self.y))
        self.proj = dest_proj

    def display(self, fig=None, extent=None, sfact=1, showfig=True, geo=False, **kwargs):
        """
        Plot ICESat tracks in a figure.

        :param fig: Figure to plot tracks in. If not set, creates a new figure.
        :param extent: Spatial extent to limit the figure to, given as xmin, xmax, ymin, ymax.
        :param sfact: Factor by which to reduce the number of points plotted.
            Default is 1 (i.e., all points are plotted).
        :param showfig: Open the figure window. Default is True.
        :param geo: Plot tracks in lat/lon coordinates, rather than projected coordinates.
            Default is False.
        :param kwargs: Optional keyword arguments to pass to matplotlib.pyplot.plot

        :type fig: matplotlib.figure.Figure
        :type extent: array-like
        :type sfact: int
        :type showfig: bool
        :type geo: bool

        :returns fig: Handle pointing to the matplotlib Figure created (or passed to display).
        """
        if fig is None:
            fig = plt.figure(facecolor='w')
            # fig.hold(True)
        # else:
            # fig.hold(True)

        if extent is None:
            extent = self.get_bounds(geo=geo)
        else:
            xmin, xmax, ymin, ymax = extent

        # if we aren't told which marker to use, pick one.
        if 'marker' not in kwargs:
            this_marker = '.'
        else:
            this_marker = kwargs['marker']
            kwargs.pop('marker')

        if geo:
            plt.plot(self.lon[::sfact], self.lat[::sfact], marker=this_marker, ls='None', **kwargs)
        else:
            plt.plot(self.x[::sfact], self.y[::sfact], marker=this_marker, ls='None', **kwargs)

        ax = fig.gca()  # get current axes
        ax.set_aspect('equal')    # set equal aspect
        ax.autoscale(tight=True)  # set axes tight
        ax.set_xlim(extent[:2])
        ax.set_ylim(extent[2:])
        
        if showfig:
            fig.show()  # don't forget this one!

        return fig
