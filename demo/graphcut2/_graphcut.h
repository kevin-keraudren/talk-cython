#include <stdio.h>
#include <iostream>
#include <cmath>
#include "graph.h"

typedef double voxel_t;

typedef double captype;
typedef double tcaptype;
typedef double flowtype;

inline size_t index( size_t i, size_t j,
                     size_t shape0, size_t shape1 ) {
    return j + shape1*i;
}

void _graphcut( voxel_t* img,
               int shape0, int shape1,
               double std,
               unsigned char* mask,
               unsigned char* seg );
