#include "_graphcut.h"

inline double _pow( double x, int a ) { return x*x; }

void _graphcut( voxel_t* img,
               int shape0, int shape1,
               double std,
               unsigned char* mask,
               unsigned char* seg ) {

    typedef Graph<captype,tcaptype,flowtype> GraphType;

    size_t nb_voxels = shape0*shape1;

    std::cout << "will create graph... " << nb_voxels  << "\n";
    GraphType *G = new GraphType( /*estimated # of nodes*/ nb_voxels,
                                  /*estimated #	of edges*/ nb_voxels*(26+1) );

    G->add_node( nb_voxels );

    double std2 = 2 * _pow( std, 2);
    
    std::cout << "building graph...\n";

    int i,j,a,b;
    size_t id, id0;
    int i0, j0, k0;
    double dist, w;
    for ( i = 0; i < shape0; i++ )
        for ( j = 0; j < shape1; j++ )
                for ( a = -1; a <= 1; a++ )
                    for ( b = -1; b <= 1; b++ ) {
                            if ( abs(a)+abs(b) == 0 )
                                continue;
                            i0 = i+a;
                            j0 = j+b;
                            if ( 0 <= i0  && i0 < shape0
                                 && 0 <= j0 && j0 < shape1 ) {
                                id = index(i,j,shape0,shape1);
                                id0 = index(i0,j0,shape0,shape1);
                                dist = sqrt( _pow( (double)(a), 2 )
                                             + _pow( (double)(b), 2 ) );
                                if ( img[id] < img[id0] )
                                    w = 1.0/dist;
                                else
                                    w = exp( - _pow(img[id] - img[id0], 2)
                                             / std2 )
                                        / dist;
                                //std::cout << w << " " << dist <<"\n";
                                G->add_edge( id,
                                             id0,
                                             w,
                                             0);
                                    }
                        }

    std::cout << "linking to source and sink...\n";
    
    for ( i = 0; i < shape0; i++ )
        for ( j = 0; j < shape1; j++ ) {
                id = index(i,j,shape0,shape1);
                if ( mask[id] == 1 )
                    G->add_tweights(id,1000,0);
                else if ( mask[id] == 2 ) 
                    G->add_tweights(id,0,1000);
            }

    std::cout << "computing maxflow...\n";
    std::cout << G->maxflow() << "\n";

    std::cout <<  "transcription of segmentation...\n";
    
    for ( i = 0; i < shape0; i++ )
        for ( j = 0; j < shape1; j++ ) {
                id = index(i,j,shape0,shape1);
                seg[id] = G->what_segment(id) + 1;
            }

    return;
}
