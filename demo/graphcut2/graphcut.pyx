import cython
import numpy as np
cimport numpy as np

np.import_array()

ctypedef double voxel_t

ctypedef double captype
ctypedef double tcaptype
ctypedef double flowtype

cdef extern from "_graphcut.h":
    void _graphcut( voxel_t*,
                   int, int,
                   double,
                   unsigned char*,
                   unsigned char* )
    
def graphcut( np.ndarray[voxel_t, ndim=2, mode="c"] img,
              np.ndarray[unsigned char, ndim=2, mode="c"] mask,
              double std ):

    cdef np.ndarray[unsigned char, 
                    ndim=2, 
                    mode="c"] seg = np.zeros( (img.shape[0],
                                               img.shape[1]),
                                              dtype='uint8')
    print "starting graphcut..."                                                                 
    _graphcut( <voxel_t*> img.data,
               img.shape[0], img.shape[1],
               std,
               <unsigned char*> mask.data,
               <unsigned char*> seg.data )
    return seg
