import numpy as np
cimport numpy as np

np.import_array()

ctypedef double captype
ctypedef double tcaptype
ctypedef double flowtype

cdef extern from "graph.h":
    cdef cppclass Graph[captype,tcaptype,flowtype]: # captype, tcaptype, flowtype
        Graph( size_t, size_t ) 
        size_t add_node(size_t)
        void add_edge(size_t,size_t,captype,captype)
        void add_tweights(size_t,tcaptype,tcaptype)
        flowtype maxflow()
        int what_segment(size_t)

cdef class PyGraph:
    # hold a C++ instance which we're wrapping
    cdef Graph[captype,tcaptype,flowtype] *thisptr    
    def __cinit__(self, size_t nb_nodes, size_t nb_edges):
        self.thisptr = new Graph[captype, tcaptype, flowtype](nb_nodes,nb_edges)
    def __dealloc__(self):
        del self.thisptr
    def add_node(self, size_t nb_nodes=1):
        self.thisptr.add_node(nb_nodes)
    def add_edge(self, size_t i, size_t j, captype cap, captype rev_cap):
        self.thisptr.add_edge(i,j,cap,rev_cap)
    def add_tweights(self, size_t i, tcaptype cap_source, tcaptype cap_sink):
        self.thisptr.add_tweights(i,cap_source,cap_sink)
    def maxflow(self):
        return self.thisptr.maxflow()
    def what_segment(self, size_t i):
        return self.thisptr.what_segment(i)
