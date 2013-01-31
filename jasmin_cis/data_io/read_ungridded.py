'''
Module for reading ungridded data in HDF4 format
'''
import numpy as np
from ungridded_data import UngriddedData
import hdf_vd as hdf_vd
import hdf_sd as hdf_sd

def get_file_variables(filename):
    '''
    Get all variables from a file containing ungridded data.
    Concatenate variable from both VD and SD data
    
    args:
        filename: The filename of the file to get the variables from
    
    '''
    SD_vars = hdf_sd.get_hdf_SD_file_variables(filename)
    VD_vars = hdf_vd.get_hdf_VD_file_variables(filename)
    
    return SD_vars, VD_vars


def get_file_coordinates(filename):
    '''
    Read in coordinate variables and pass back tuple of lat, lon,
    each element of tuple being a 2D numpy array
    '''

    data = hdf_vd.get_hdf4_VD_data(filename,['Latitude','Longitude'])
    lat = data['Latitude'].get()
    long = data['Longitude'].get()
    
    return (lat,long)


def get_file_coordinates_points(filename):
    '''
    Convert coordinate arrays into a list of points
    useful or colocation sampling   
    '''
    from jasmin_cis.data_io.hyperpoint import HyperPoint
    
    latitude, longitude = get_file_coordinates(filename)
    
    points = []    
    
    for (x,y), lat in np.ndenumerate(latitude):
        lon = longitude[x,y]
        points.append(HyperPoint(lat,lon))
        
    return points


def read(filenames, variables):
    '''
    Read ungridded data from a file. Just a wrapper that calls the UngriddedData class method
    
        @param filename:     A name of a file to read
        @param variables:    List of variables to read from the files
        
        @return A list of ungridded data objects 
    '''
    return UngriddedData.load_ungridded_data(filenames, variables)           

def read_hdf4(filename,variables):
    '''
        A wrapper method for reading raw data from hdf4 files. This returns a dictionary of io handles
         for each VD and SD data types.
       
        @param filename:     A name of a file to read
        @param variables:    List of variables to read from the files
        
        @return (sds_dict, vds_dict) A tuple of dictionaries, one for sds objects and another for vds 
    '''
    from pyhdf.error import HDF4Error
    from jasmin_cis.exceptions import FileIOError

    variables = variables + ['Latitude','Longitude','TAI_start','Profile_time', 'Height']
    
    sds_dict = {}
    vds_dict = {}

    try:
        sds_dict = hdf_sd.read_sds(filename,variables)
    except HDF4Error as e:
        try:
            vds_dict = hdf_vd.read_vds(filename,variables)
        except:
            raise FileIOError(str(e)+' for file: '+filename)
    return sds_dict, vds_dict
