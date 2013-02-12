from nose.tools import istest, raises
import numpy
from data_io.Coord import Coord, CoordList
from data_io.ungridded_data import Metadata
from jasmin_cis.exceptions import DuplicateCoordinateError

def create_dummy_coordinates_list():
    coord1 = Coord(numpy.array([5,4]),Metadata(standard_name='testY'),axis='Y')
    coord2 = Coord(numpy.array([5,4]),Metadata(standard_name='testX'),axis='X')
    return CoordList([coord1,coord2])

@istest
def can_create_a_valid_list_of_coordinates():
    list = create_dummy_coordinates_list()
    assert(len(list)==2)
    assert(list[0].standard_name=='testY')
    assert(list[1].standard_name=='testX')
    assert(list[0].axis=='Y')
    assert(list[1].axis=='X')

@istest
def can_append_to_list_of_coordinates():
    list = create_dummy_coordinates_list()
    list.append(Coord(numpy.array([5,4]),Metadata(standard_name='testZ'),axis='Z'))
    assert(len(list)==3)
    assert(list[2].standard_name=='testZ')
    assert(list[2].axis=='Z')

@istest
@raises(DuplicateCoordinateError)
def append_a_duplicate_to_a_list_of_coordinates_fails():
    list = create_dummy_coordinates_list()
    list.append(Coord(numpy.array([5,4]),Metadata(standard_name='testX'),axis='X'))

@istest
def can_find_a_coord_from_a_list_of_coordinates():
    list = create_dummy_coordinates_list()
    coord = list.get_coord(standard_name='testX')
    assert(coord.standard_name=='testX')
    assert(coord.axis=='X')

@istest
def can_find_many_coords_from_a_list_of_coordinates():
    list = create_dummy_coordinates_list()
    list.append(Coord(numpy.array([5,4]),Metadata(name='testZ'),axis='Z'))
    list.append(Coord(numpy.array([5,4]),Metadata(name='testZ')))
    assert(len(list)==4)
    coords = list.get_coords(name='testZ')
    assert(len(coords)==2)
    assert(coords[0].name()=='testZ')
    assert(coords[0].axis=='Z')
    assert(coords[1].axis=='')