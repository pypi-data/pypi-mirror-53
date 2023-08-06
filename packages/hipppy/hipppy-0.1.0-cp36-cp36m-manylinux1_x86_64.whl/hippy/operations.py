"""This module contains hip functionnalities
    intending to perform mesh operations
"""
from hippy import hip_cmd


def generate_2d_mesh(lower_corner, upper_corner, resolution):
    """Generate an unstructured rectangular mesh
       of quadrilateral elements given box bounds

       Parameters:
       ==========
       lower_corner: A tuple/list of box lower corner
                     coordinates (x, y)
       upper_corner: A tuple/list of box upper corner
                     coordinates (x, y)
       resolution : a tuple/list of mesh resolution
                    (i.e number of points) (n_x, n_y)
    """
    command = "%f %f %f %f %d %d" %(lower_corner[0],
                                    lower_corner[1],
                                    upper_corner[0],
                                    upper_corner[1],
                                    resolution[0],
                                    resolution[1])
    command = "generate %s" %command
    hip_cmd(command)

def extrude_2d_mesh(extrude_coords, extrude_node_num, axis):
    """ Extrude 2-dimensional mesh to a 3D mesh.

        Parameters:
        ==========
        extrude_coords: a tuple/list of extrusion extremes
                        (ext_min, ext_max), ext_min and ext_max
                        can refer to positions (if extusion is
                        done around x, y or z axis) or to angles
                        in degrees (if extusion is choosen to be
                        axisymmetric)
        extrude_node_num: Number of nodes/elements slices
        axis: axis around which extrusion is performed, possible
              values :
               - x, y, z or axi
    """
    command = 'copy 3D %f, %f, %d, %s' %(extrude_coords[0],
                                         extrude_coords[1],
                                         extrude_node_num,
                                         axis)
    hip_cmd(command)

# def test_mesh_gen():
#     from hip_writers import write_ensight
#     lower_corner = (0, 0.5)
#     upper_corner = (1, 1)
#     resolution = (10, 10)
#     extrude_coords = [0, 120]
#     extrude_node_num = 100
#     axis = "s"
#     generate_2d_mesh(lower_corner, upper_corner, resolution)
#     print("kaka")
#     # write_ensight("./tests/test_box")
#     extrude_2d_mesh(extrude_coords, extrude_node_num, axis)
#     write_ensight("./tests/test_box_extrude")

# test_mesh_gen()
# copy uns
# mm/ adapt
# interpolate
# transform
