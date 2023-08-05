//Define basic types from CGAL templates
#include <CGAL/Exact_predicates_inexact_constructions_kernel.h>
#include <CGAL/Cartesian.h>
#include <CGAL/Regular_triangulation_3.h>
#if CGAL_VERSION_NR < CGAL_VERSION_NUMBER(4,11,0)
    #include <CGAL/Regular_triangulation_euclidean_traits_3.h>
#endif

#include <CGAL/Triangulation_vertex_base_with_info_3.h>
#include <CGAL/Triangulation_cell_base_with_info_3.h>
#include <CGAL/Delaunay_triangulation_3.h>
#include <CGAL/circulator.h>
#include <CGAL/number_utils.h>
#include <boost/static_assert.hpp>

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>

#include "connectivityMatrix.hpp"

namespace py = pybind11;


//This include from yade let us use Eigen types
// #include <lib/base/Math.hpp>

//const unsigned facetVertices [4][3] = {{1,2,3},{0,2,3},{0,1,3},{0,1,2}};
////return the opposite edge (e.g. the opposite of {0,2} is {1,3})
//inline void revertEdge (unsigned &i,unsigned &j){
//    if (facetVertices[i][0]==j) {i=facetVertices[i][1];j=facetVertices[i][2];}
//    else if (facetVertices[i][1]==j) {i=facetVertices[i][0];j=facetVertices[i][2];}
//    else {j=facetVertices[i][1]; i=facetVertices[i][0];}
//}

typedef CGAL::Exact_predicates_inexact_constructions_kernel K;

#if CGAL_VERSION_NR < CGAL_VERSION_NUMBER(4,11,0)
    typedef CGAL::Regular_triangulation_euclidean_traits_3<K>   Traits;
#else
    typedef K                                                   Traits;
#endif

typedef K::Point_3                                              Point;
#if CGAL_VERSION_NR < CGAL_VERSION_NUMBER(4,11,0)
    typedef Traits::RT                                          Weight;
    typedef Traits::Weighted_point                              Weighted_point;
#else
    typedef Traits::FT                                          Weight;
    typedef Traits::Weighted_point_3                            Weighted_point;
#endif
typedef Traits::Plane_3                                         Plane;
typedef Traits::Triangle_3                                      Triangle;
typedef Traits::Tetrahedron_3                                   Tetrahedron;

#if CGAL_VERSION_NR < CGAL_VERSION_NUMBER(4,11,0)
    typedef CGAL::Triangulation_vertex_base_with_info_3<unsigned, Traits>       Vb_info;
    typedef CGAL::Triangulation_cell_base_with_info_3<unsigned, Traits>         Cb_info;
#else
    typedef CGAL::Regular_triangulation_vertex_base_3<K>                        Vb0;
    typedef CGAL::Regular_triangulation_cell_base_3<K>                          Rcb;
    typedef CGAL::Triangulation_vertex_base_with_info_3<unsigned, Traits, Vb0>  Vb_info;
    typedef CGAL::Triangulation_cell_base_with_info_3<unsigned, Traits, Rcb>    Cb_info;
#endif

typedef CGAL::Triangulation_data_structure_3<Vb_info, Cb_info>  Tds;
typedef CGAL::Triangulation_3<K>                                Triangulation;
typedef CGAL::Regular_triangulation_3<Traits, Tds>              RTriangulation;

// extern "C"

int countTetrahedraCGAL( py::array_t<float> numTetrahedrals_verticesNumpy,
                         py::array_t<float> numTetrahedrals_weightsNumpy)
{

  py::buffer_info numTetrahedrals_verticesBuf = numTetrahedrals_verticesNumpy.request();
  py::buffer_info numTetrahedrals_weightsBuf = numTetrahedrals_weightsNumpy.request();

  float *numTetrahedrals_vertices = (float*) numTetrahedrals_verticesBuf.ptr;
  float *numTetrahedrals_weights = (float*) numTetrahedrals_weightsBuf.ptr;

  int numTetrahedrals_numVertices = (int) numTetrahedrals_verticesBuf.shape[0];

    float x,y,z;
    std::vector<std::pair<Weighted_point,unsigned>> points;

    // create point pairs and delaunay triangulate
    for (int i=0; i<numTetrahedrals_numVertices; i++)
    {
        z = (float)numTetrahedrals_vertices[3*i+0];
        y = (float)numTetrahedrals_vertices[3*i+1];
        x = (float)numTetrahedrals_vertices[3*i+2];
        Point p(z,y,x);
        Weight w=(float)numTetrahedrals_weights[i];
        points.push_back(std::make_pair(Weighted_point(p,w),i));
    }
    RTriangulation T(points.begin(),points.end());

    CGAL_assertion(T.number_of_vertices() == numTetrahedrals_numVertices);

    return (uint32_t)T.number_of_finite_cells();
}


void triangulateCGAL(   py::array_t<float> connectivityMatrix_verticesNumpy,
                        py::array_t<float> connectivityMatrix_weightsNumpy,
                        py::array_t<unsigned int> connectivityMatrix_connectivityNumpy)
{

  py::buffer_info connectivityMatrix_verticesBuf = connectivityMatrix_verticesNumpy.request();
  py::buffer_info connectivityMatrix_weightsBuf = connectivityMatrix_weightsNumpy.request();
  py::buffer_info connectivityMatrix_connectivityBuf = connectivityMatrix_connectivityNumpy.request();

  float *connectivityMatrix_vertices = (float*) connectivityMatrix_verticesBuf.ptr;
  float *connectivityMatrix_weights = (float*) connectivityMatrix_weightsBuf.ptr;
  unsigned int *connectivityMatrix_connectivity = (unsigned int*) connectivityMatrix_connectivityBuf.ptr;

  int connectivityMatrix_numVertices = (int) connectivityMatrix_verticesBuf.shape[0];


    float x,y,z;
    std::vector<std::pair<Weighted_point,unsigned>> points;

    // create point pairs and delaunay triangulate
    for (int i=0; i<connectivityMatrix_numVertices; i++)
    {
        z = (float)connectivityMatrix_vertices[3*i+0];
        y = (float)connectivityMatrix_vertices[3*i+1];
        x = (float)connectivityMatrix_vertices[3*i+2];
        Point p(z,y,x);
        Weight w=(float)connectivityMatrix_weights[i];
        points.push_back(std::make_pair(Weighted_point(p,w),i));
        //std::cout<<"Point made "<<x << " " << " " << y << " " << z << " id " << i << std::endl;
    }
    RTriangulation T(points.begin(),points.end());

    CGAL_assertion(T.number_of_vertices() == connectivityMatrix_numVertices);

//     check that the info was correctly set
//    RTriangulation::Finite_vertices_iterator vit;
//    for (vit = T.finite_vertices_begin(); vit != T.finite_vertices_end(); ++vit)
//        if( points[vit->info()-1].second != vit->info() && points[vit->info()-1].first != vit->point()){
//        //std::cerr << "Error id info incorrect,  " << std::endl;
//        exit(EXIT_FAILURE);
//    }
//     std::cout << "Points correctly set with id" << std::endl;

    // iterate on cells to generate numCellsx4 connectivity matrix
    RTriangulation::Finite_cells_iterator cit; uint32_t tetNumber = 0;
    for (cit = T.finite_cells_begin(); cit != T.finite_cells_end(); cit++)
    {
        for (uint32_t i=0;i<4;i++)
        {
            connectivityMatrix_connectivity[4*tetNumber+i] = (uint32_t) cit->vertex(i)->info();
        }
        tetNumber += 1;
    }
}
