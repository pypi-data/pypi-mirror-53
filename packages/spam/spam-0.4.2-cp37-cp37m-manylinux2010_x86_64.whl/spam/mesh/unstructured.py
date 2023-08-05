from __future__ import print_function
"""This module offers a set of tools for unstructured 3D meshes made of tetrahedra.

>>> # import module
>>> import spam.mesh
>>> spam.mesh.createCuboid()


WARNING
-------
    System dependencies
        * ``gmsh``
    Python dependencies
        * ``pygmsh``
        * ``meshio``
"""
import numpy
import spam.mesh


def createCuboid(lengths, lcar, origin=[0., 0., 0.], verbose=False, gmshFile=None, vtkFile=None):
    """
    Creates an unstructured mesh of tetrahedra inside a cuboid.

    Parameters
    ----------
        lengths: 1D array
            The lengths of the cuboid in the three directions
            The axis order is zyx

        origin: 1D array
            The origin of the cuboid (zyx)

        lcar: float
            characteristic length of the elements of the mesh
            (`i.e.`, the average distance between two nodes)

        gmshFile: string, optional
            If not None, save the clear text gmsh file with name ``gmshFile`` and suffix ``.msh``
            Default = None

        vtkFile: string, optional
            If not None, save the clear text vtk file with name ``vtkFile`` and suffix ``.vtk``
            Defaut = None

        verbose: bool, optionsl
            Verbose mode.
            Default = False

    Returns
    -------
        points: 2D numpy array
            The coordinates of the mesh nodes (zyx)
            Each line is [zPos, yPos, xPos]

        connectivity: 2D numpy array
            The connectivity matrix of the tetrahedra elements
            Each line is [node1, node2, node3, node4]

    Example
    -------
        >>> points, connectivity = spam.mesh.createCuboid((1.0,1.5,2.0), 0.5)
        create a mesh in a cuboid of size 1,1.5,2 with a characteristic length of 0.5
    """

    import pygmsh
    import meshio

    # We will switch the input arrays from zyx to xyz before passing them to pygmsh
    lengths = lengths[::-1]
    origin = origin[::-1]

    lx, ly, lz = lengths
    ox, oy, oz = origin
    geom = pygmsh.built_in.Geometry()
    poly = geom.add_polygon([[ox, ly + oy, oz],
                             [lx + ox, ly + oy, oz],
                             [lx + ox, oy, oz],
                             [ox, oy, oz]], lcar=lcar)
    geom.extrude(poly, translation_axis=[0., 0., lz])

    # create mesh and get connectivity
    # points, cells, _, _, _ = pygmsh.generate_mesh(geom, verbose=verbose, extra_gmsh_arguments=['mesh.Algorithm3D=4', '-optimize_netgen'])
    # points, cells, _, _, _ = pygmsh.generate_mesh(geom, verbose=verbose, extra_gmsh_arguments=["-optimize", "-algo", "del3d", "-clmin", str(lcar), "-clmax", str(lcar)])
    mesh = pygmsh.generate_mesh(geom, verbose=verbose, extra_gmsh_arguments=["-optimize", "-algo", "del3d", "-clmin", str(lcar), "-clmax", str(lcar)])
    points = mesh.points
    cells = mesh.cells
    connectivity = cells['tetra']

    # write gmsh/vtk file
    if gmshFile is not None:
        meshio.write_points_cells("{}.msh".format(gmshFile), points, cells, file_format='gmsh2-ascii')
    if vtkFile is not None:
        meshio.write_points_cells("{}.vtk".format(vtkFile), points, {'tetra': connectivity}, file_format='vtk-binary')

    # NOTE: pygmsh returns coordinates in xyz. This means that:
    # 1. the coordinates array must be switched back to zyx
    # 2. the connectivity array must change so that the nodes of each tetrahedron are numbered
    #    in such a way that the Jacobian is positive. Which means a perturbation of the node numbering.

    points = points[:, ::-1]
    tmp = connectivity.copy()
    connectivity[:, 1] = tmp[:, 3]
    connectivity[:, 3] = tmp[:, 1]

    # return coordinates and connectivity matrix
    return points, connectivity


def createCylinder(centre, radius, height, lcar, verbose=False, gmshFile=None, vtkFile=None):
    """
    Creates an unstructured mesh of tetrahedra inside a cylinder.
    The height of the cylinder is along the z axis.

    Parameters
    ----------
        centre: 1D array
            The two coordinates of the centre of the base disk (yx).

        radius: float
            The radius of the base disk.

        height: float
            The height of the cylinder of the z direction.

        lcar: float
            length of the mesh.
            The average distance between two nodes.

        gmshFile: string, optional
            If not None, save the clear text gmsh file with name ``gmshFile`` and suffix ``.msh``
            Default = None

        vtkFile: string, optional
            If not None, save the clear text vtk file with name ``vtkFile`` and suffix ``.vtk``
            Defaut = None

        verbose: bool, optionsl
            Verbose mode.
            Default = False

    Returns
    -------
        points: 2D numpy array
            The coordinates of the mesh nodes (zyx)
            Each line is [zPos, yPos, xPos]

        connectivity: 2D numpy array
            The connectivity matrix of the tetrahedra elements
            Each line is [node1, node2, node3, node4]

    Example
    -------
        >>> points, connectivity =  spam.mesh.createCylinder((0.0,0.0), 0.5, 2.0, 0.5)
        create a mesh in a cylinder of centre 0,0,0 radius, 0.5 and height 2.0 with a characteristic length of 0.5
    """

    import pygmsh
    import meshio

    # unpack
    cy, cx = centre
    r = radius

    # raw code
    code = []
    code.append("Point(1) = {{ {x}, {y},  0, {lcar} }};".format(x=cx, y=cy, lcar=lcar))
    code.append("Point(2) = {{ {x}, {y},  0, {lcar} }};".format(x=cx + r, y=cy, lcar=lcar))
    code.append("Point(3) = {{ {x}, {y},  0, {lcar} }};".format(x=cx, y=cy + r, lcar=lcar))
    code.append("Point(4) = {{ {x}, {y},  0, {lcar} }};".format(x=cx - r, y=cy, lcar=lcar))
    code.append("Point(5) = {{ {x}, {y},  0, {lcar} }};".format(x=cx, y=cy - r, lcar=lcar))
    code.append("Circle(1) = { 2, 1, 3 };")
    code.append("Circle(2) = { 3, 1, 4 };")
    code.append("Circle(3) = { 4, 1, 5 };")
    code.append("Circle(4) = { 5, 1, 2 };")
    code.append("Line Loop(5) = { 1, 2, 3, 4 };")
    code.append("Plane Surface(6) = { 5 };")
    code.append("Extrude {{ 0, 0, {h} }} {{ Surface{{ 6 }}; }}".format(h=height))

    # geom = pygmsh.opencascade.Geometry(characteristic_length_min=lcar, characteristic_length_max=lcar,)

    # add raw code to geometry
    geom = pygmsh.built_in.Geometry()
    geom.add_raw_code(code)

    # mesh
    # points, cells, _, _, _ = pygmsh.generate_mesh(geom, verbose=verbose, extra_gmsh_arguments=["-optimize_netgen"])
    # points, cells, _, _, _ = pygmsh.generate_mesh(geom, verbose=verbose, extra_gmsh_arguments=["-optimize","-algo","del3d","-clmin",str(lcar),"-clmax",str(lcar)])
    mesh = pygmsh.generate_mesh(geom, verbose=verbose, extra_gmsh_arguments=["-optimize", "-algo", "del3d", "-clmin", str(lcar), "-clmax", str(lcar)])
    points = mesh.points
    cells = mesh.cells
    connectivity = cells['tetra']

    # write gmsh/vtk file
    if gmshFile is not None:
        meshio.write_points_cells("{}.msh".format(gmshFile), points, cells, file_format='gmsh2-ascii')
    if vtkFile is not None:
        meshio.write_points_cells("{}.vtk".format(vtkFile), points, {'tetra': connectivity}, file_format='vtk-ascii')

    # NOTE: pygmsh returns coordinates in xyz. This means that:
    # 1. the coordinates array must be switched back to zyx
    # 2. the connectivity array must change so that the nodes of each tetrahedron are numbered
    #    in such a way that the Jacobian is positive. Which means a perturbation of the node numbering.

    points = points[:, ::-1]
    tmp = connectivity.copy()
    connectivity[:, 1] = tmp[:, 3]
    connectivity[:, 3] = tmp[:, 1]

    # return coordinates and connectivity matrix
    return points, connectivity

def triangulate(coordinates, weights=None):
    """
    Takes a series of coordinates and optionally their weights and returns a tetrahedral connectivity matrix.
    This function uses CGAL's Regular Triangulation the background (with all weights=1 if they are not passed).
    Weights are passed to CGAL's Regular Triangulation directly and so should be squared if they are radii of particles.

    Parameters
    ----------
        coordinates : Nx3 2D numpy array of floats
            N points to triangulate (Z, Y, X)

        weights : numpy vector of N floats
            list of weights associated with coordinates.
            Default = None (which means all weights=1).

    Returns
    -------
        connectivityMatrix : Mx4 numpy array of unsigned ints
            delaunay triangulation with each row containing point numbers

    Note
    ----
        Code from Robert Caulk

    """
    # There are two passes here -- CGAL is all based in templates, and just stores the triangulation
    #   in a smart way.
    # We want the connectivity matrix, which CGAL doesn't know about, so we use a first pass to get the
    #   number of tetrahedra, so that we can allocate the connectivity matrix in python, and pass it to
    #   the next pass through the code, which fills the connectivity matrix
    import spam.mesh.meshToolkit as mtk

    if weights is None:
        weights = numpy.ones(len(coordinates))

    elif weights.shape[0] != coordinates.shape[0]:
        raise Exception("weights array dim1 != coordinates array dim1")

    coordinates = coordinates.astype('<f4')
    weights = weights.astype('<f4')

    # get the number of tetrahedra so we can properly size our connectivityMatrix
    # labelToolkit.numTetrahedrals.restype  = c_int
    # labelToolkit.numTetrahedrals.argtypes = [c_int,
    # numpy.ctypeslib.ndpointer(dtype=numpy.float32, ndim=2, flags='CONTIGUOUS'),
    # numpy.ctypeslib.ndpointer(dtype=numpy.float32, ndim=1, flags='CONTIGUOUS')]
    nTet = mtk.countTetrahedraCGAL(coordinates, weights)
    connMat = numpy.zeros([nTet, 4], dtype='<u4')

    # setup the return types and argument types
    # labelToolkit.connectivityMatrix.restype  = None
    # labelToolkit.connectivityMatrix.argtypes = [c_int,
    # numpy.ctypeslib.ndpointer(dtype=numpy.float32, ndim=2, flags='CONTIGUOUS'),
    # numpy.ctypeslib.ndpointer(dtype=numpy.float32, ndim=1, flags='CONTIGUOUS'),
    # numpy.ctypeslib.ndpointer(dtype=numpy.uint32,  ndim=2, flags='CONTIGUOUS')]
    mtk.triangulateCGAL(coordinates, weights, connMat)

    return connMat


def bagiStrain(coordinates, connectivity, displacements, largeStrains=True, onlyStrain=True):
    """
    Calculates displacement gradient function using Bagi's 1996 paper, especially equantion 3 on page 174.
    Required inputs are connectivity matrix for tetrahdra (for example from spam.mesh.delaunayFromVoronoi) and
    nodal positions in reference and deformed configurations.

    Parameters
    ----------
        coordinates : m x 3 numpy array
            M Particles' coordinates in reference configuration

        connectivity : n x 4 numpy array
            Delaunay triangulation connectivity generated by spam.mesh.delaunayFromVoronoi for example

        displacements : m x 3 numpy array
            M Particles' displacement

        largeStrains: bool, optional
            Use Large/finite strains framework (recommended)?
            Default = True

        onlyStrain: bool, optional
            Output only only strain components?
            Otherwise also output F and R from the decomposition of U
            Default = True

    Returns
    -------
        strainTensor: nx3x3 array of n cells
            The full strain field
            If `largeStrains = True` it is the decomposed right stretch tensor U - I
            If `largeStrains = False` it is the small strain symmetric tensor
            Its shape is (nz, ny, nx, 3, 3)

        F: nx3x3 array of n cells
            The field of the transformation gradient tensors
            Its shape is (nz, ny, nx, 3, 3)
            Only if `onlyStrain = False`

        r: nx3x1 array of n cells
            Rotation in "rotation vector" format
            Its shape is (nz, ny, nx, 3)
            Only if onlyStrain=False and largeStrains=True

        volStrain: nx1 array of n cells strain tensors
            The volumetric strain field
            If `largeStrains = True` it is the determinant of the transformation gradient tensor: norm(F) - 1
            If `largeStrains = False` it is the trace of the small strain symmetric tensor
            Its shape is (nz, ny, nx)

        devStrain: nx1 array of n cells strain tensors
            The deviatoric strain field
            If `largeStrains = True` it is the norm of the deviatoric part of the right stretch tensor U
            If `largeStrains = False` ?
            Its shape is (nz, ny, nx)

    """
    from progressbar import ProgressBar
    pbar = ProgressBar()

    if largeStrains:
        # print("\n*** The strain field is computed under the hypothesis of large strains ***")
        smallStrains = False
        F = numpy.zeros([connectivity.shape[0], 3, 3], dtype='<f4')
        U = numpy.zeros([connectivity.shape[0], 3, 3], dtype='<f4')
        R = numpy.zeros([connectivity.shape[0], 3], dtype='<f4')
        volStrain = numpy.zeros(connectivity.shape[0], dtype='<f4')
        devStrain = numpy.zeros(connectivity.shape[0], dtype='<f4')
    else:
        # print("\n*** The strain field is computed under the hypothesis of small strains ***")
        smallStrains = True
        F = numpy.zeros([connectivity.shape[0], 3, 3], dtype='<f4')
        e = numpy.zeros([connectivity.shape[0], 3, 3], dtype='<f4')
        volStrain = numpy.zeros(connectivity.shape[0], dtype='<f4')
        devStrain = numpy.zeros(connectivity.shape[0], dtype='<f4')

    connectivity = connectivity.astype(numpy.uint)

    # define dimension
    D = 3.0

    # Import modules

    # Construct 4-list of 3-lists of combinations constituting a face of the tet
    combs = [[0, 1, 2],
             [1, 2, 3],
             [2, 3, 0],
             [0, 1, 3]]
    unode = [3, 0, 1, 2]

    # Precompute tetrahedron Volumes
    tetVolumes = spam.mesh.tetVolumes(coordinates, connectivity)

    # Initialize arrays for tet strains
    # print("spam.mesh.bagiStrain(): Constructing strain from Delaunay and Displacements")

    # Loop through tetrahdra to get avec1, uPos1
    # for tet in range(connectivity.shape[0]):
    for tet in pbar(range(connectivity.shape[0])):
        # Get the list of IDs, centroids, center of tet
        tet_ids = connectivity[tet, :]
        tetCoords = coordinates[tet_ids, :]
        tetDisp = displacements[tet_ids, :]
        tetCen = numpy.average(tetCoords, axis=0)

        # Loop through each face of tet to get avec, upos (Bagi, 1996, pg. 172)
        # aVec1 = numpy.zeros([4, 3], dtype='<f4')
        # uPos1 = numpy.zeros([4, 3], dtype='<f4')
        # uPos2 = numpy.zeros([4, 3], dtype='<f4')
        displacementGradient = numpy.zeros((3, 3), dtype='<f4')

        for face in range(4):
            faceNorm = numpy.cross(tetCoords[combs[face][0]] - tetCoords[combs[face][1]],
                                   tetCoords[combs[face][0]] - tetCoords[combs[face][2]])

            # Get a norm vector to face point towards center of tet
            faceCen = numpy.average(tetCoords[combs[face]], axis=0)
            tmpnorm = faceNorm / (numpy.linalg.norm(faceNorm))
            facetocen = tetCen - faceCen
            if (numpy.dot(facetocen, tmpnorm) < 0):
                tmpnorm = -tmpnorm

            # Divide by 6 (1/3 for 1/Dimension; 1/2 for area from cross product)
            # See first eqn., Bagi, 1996, pg. 172.
            # aVec1[face] = tmpnorm*numpy.linalg.norm(faceNorm)/6

            # Undeformed positions
            # uPos1[face] = tetCoords[unode[face]]
            # Deformed positions
            # uPos2[face] = tetComs2[unode[face]]

            displacementGradient += numpy.tensordot(tetDisp[unode[face]], tmpnorm * numpy.linalg.norm(faceNorm) / 6, axes=0)

        displacementGradient /= float(tetVolumes[tet])

        # Compute strains
        if largeStrains:
            F[tet], U[tet], R[tet], volStrain[tet], devStrain[tet] = spam.mesh.decomposeDisplacementGradientLargeStrain(displacementGradient)
        else:
            F[tet], e[tet], volStrain[tet], devStrain[tet] = spam.mesh.decomposeDisplacementGradientSmallStrain(displacementGradient)

    if largeStrains:
        if onlyStrain:
            return (U - numpy.eye(3), volStrain, devStrain)
        else:
            return (U - numpy.eye(3), F, R, volStrain, devStrain)
    elif smallStrains:
        if onlyStrain:
            return (e, volStrain, devStrain)
        else:
            return (e, F, volStrain, devStrain)


def projectTetFieldToGrains(connectivity, tetField, com2):
    """
    Projects/coarse-grains any field defined on tetrahedra onto grains by volume-averaging over
    all tetrahedra for which a given grain is a node.
    This can be useful for smoothing out a noisy strain field and will not affect the overall agreement between
    the average of strains and the macroscopically observed strains (R.C. Hurley has verified this in a 2017 paper).

    Parameters
    ----------
        connectivity: n x 4 numpy array
            Delaunay triangulation connectivity generated by spam.mesh.delaunayFromVoronoi for example

        tetField: n x 3 x 3 numpy array
            Any field defined on tetrahedra (e.g., Bagi strains from bagiStrain).

        com2: m x 3 numpy array
            M Particles' coordinates (in deformed configuration for strain field)

    Returns
    -------
        grainField: m x 3 x 3
            array containing (3x3) arrays of strain

    Example
    -------
        grainStrain = spam.mesh.projectBagiStrainToGrains(connectivity,bagiStrain[0],com2)
            Returns strains for each grain.

    Notes
    ------
        Code from Ryan Hurley

    """
    # grainStrainVoigt:  Ng array containing (6x1) arrays of strain in Voigt notation.
    # RCH Oct 2018.

    # Import modules
    import numpy
    import scipy.spatial as sps
    from progressbar import ProgressBar
    pbar = ProgressBar()

    # print("spam.mesh.projectTetFieldToGrains(): Pre-computing volumes...", end='')
    tetVolumes2 = spam.mesh.tetVolumes(com2, connectivity)
    # print("done.")

    # Initialize list of grain values
    grainField = numpy.zeros(([com2.shape[0]] + list(tetField.shape[1:])), dtype='<f4')
    # Get all the unique grain IDs in the Deluanay triangulation

    # print("spam.mesh.projectTetFieldToGrains(): Projecting tetrahedal to grains...")
    # Loop through grains...
    # for label in pbar(range(com2.shape[0])):
    for label in range(com2.shape[0]):
        # Get the list of tets for which this label is a node
        touchingTets = numpy.where(connectivity == label)[0]

        volTot = 0.0
        fieldTot = numpy.zeros(list(tetField.shape[1:]), dtype='<f4')
        # Loop through list of tets, summing the strains
        for touchingTet in touchingTets:
            vol = tetVolumes2[touchingTet]
            # Track total volume
            volTot += vol

            # Add volume-weighted field
            fieldTot += tetField[touchingTet] * vol

        # Divide strainTot by volTot
        fieldTot = fieldTot / volTot

        # Store in particles
        grainField[label] = fieldTot

    return(grainField)


def _projectBagiStrainToGrid(connectivity, tet_strain, com2, nx=8, ny=8, nz=10):
    """
    Projects/coarse-grains strains from tetrahedra onto a grid. The first step is
        constructing a Cartesian grid based on the extremal positions of all tetrahedra
        nodes. The next step is finding all tetrahedra having a node within each grid cell.
        the final step is volume-averaging over all of the corresponding tetrahedra.

    Parameters
    ----------
        connectivity: n x 4 numpy array
            Delaunay triangulation connectivity generated by spam.mesh.delaunayFromVoronoi for example

        tet_strain: n x 3 x 3 numpy array
            Tetrahedra strail from spam.mesh.bagiStrain. This can be
            either tetStrainsSym or tetStrainAsym. The resulting projected/coarse-grained
            will be either the symmetric or skew-symmetric strain, respectively

        com2: m x 3 numpy array
            M Particles' coordinates in deformed configuration

    Returns
    -------
        gridStrain:
            Ng array containing (3x3) arrays of strain. (Ng = number of grains)

    Example
    -------
        grid_bounds,num_in_grid,gridStrain
            = spam.mesh.projectBagiStrainToGrid(connectivity,tet_strain,com2,nx,ny,nz)
            Returns strains for each grid zone and boundaries of grid zone.

    """
    # gridStrainVoigt:  Ng array containing (6x1) arrays of strain in Voigt notation.
    # RCH Oct 2018.

    # Import modules
    import numpy
    import scipy.spatial as sps
    from progressbar import ProgressBar
    pbar = ProgressBar()

    # Artificial edge buffer to make sure we grab the outer-most particles
    edgeBuf = 0.01

    # Get sample extents for grid
    edges = numpy.array([[com2[:, 0].min() - edgeBuf, com2[:, 0].max() + edgeBuf],
                         [com2[:, 1].min() - edgeBuf, com2[:, 1].max() + edgeBuf],
                         [com2[:, 2].min() - edgeBuf, com2[:, 2].max() + edgeBuf]])

    # Construct grid with convention xmin,xmax,ymin,ymax,zmin,zmax
    grid_bounds = []
    xspace = (edges[0, 1] - edges[0, 0]) / (nx)
    yspace = (edges[1, 1] - edges[1, 0]) / (ny)
    zspace = (edges[2, 1] - edges[2, 0]) / (nz)
    for ii in range(nz):
        for jj in range(nx):
            for kk in range(ny):
                grid_bounds.append(numpy.array([edges[0, 0] + jj * xspace, edges[0, 0] + (jj + 1) * xspace,
                                                edges[1, 0] + kk * yspace, edges[1, 0] + (kk + 1) * yspace,
                                                edges[2, 0] + ii * zspace, edges[2, 0] + (ii + 1) * zspace]))
    grid_bounds = numpy.array(grid_bounds)

    # Initialize list of tet strains
    gridStrain = []
    # gridStrainVoigt = []
    # First, find all grains in each grid:
    print("spam.mesh.projectBagiStrainToGrid(): Projecting tetrahedal field to grid...\n")
    for ii in pbar(range(grid_bounds.shape[0])):
        xcond = numpy.logical_and(com2[:, 0] > grid_bounds[ii, 0], com2[:, 0] <= grid_bounds[ii, 1])
        ycond = numpy.logical_and(com2[:, 1] > grid_bounds[ii, 2], com2[:, 1] <= grid_bounds[ii, 3])
        zcond = numpy.logical_and(com2[:, 2] > grid_bounds[ii, 4], com2[:, 2] <= grid_bounds[ii, 5])
        indgrain = numpy.where(numpy.logical_and(xcond, numpy.logical_and(ycond, zcond)))

        # Find all tets for which these grains act as a node:
        indtet = []
        for jj in range(indgrain[0].shape[0]):
            indtettmp, _ = numpy.where(connectivity == indgrain[0][jj])
            for kk in range(indtettmp.shape[0]):
                indtet.append(indtettmp[kk])

        # Find unique values of these tets
        indtet = numpy.unique(indtet, return_index=False)

        # Loop over unique tets to get volume-averaged strains
        volTot = 0.0
        strainTot = numpy.zeros((3, 3))
        num_in_grid = []
        num_in_grid_tmp = 0
        if (indtet.shape[0] > 0):
            for jj in range(indtet.shape[0]):
                # Get volume
                tet_ids = connectivity[indtet[jj], :]
                tetCoords = com2[tet_ids, :]
                cvxh = sps.ConvexHull(tetCoords)
                vol = cvxh.volume

                # Add volume and strain
                strainTot = strainTot + tet_strain[indtet[jj]] * vol
                volTot = volTot + vol

            # Divide strainTot by volTot
            strainTot = strainTot / volTot
            num_in_grid_tmp = num_in_grid_tmp + indtet.shape[0]

        # Store in grid
        num_in_grid.append(num_in_grid_tmp)
        gridStrain.append(numpy.array(strainTot))
        # gridStrainVoigt.append(numpy.array([strainTot[0, 0], strainTot[1, 1], strainTot[2, 2],
        # strainTot[1, 2], strainTot[0, 2], strainTot[0, 1]]))

    # return(grid_bounds, num_in_grid, gridStrain, gridStrainVoigt)
    return(grid_bounds, num_in_grid, gridStrain)


def BCFieldFromDVCField(meshNodes, dvcField, mask=None, pixelSize=1.0, meshType="cube", centre=[0, 0], radius=1.0, topBottom=False, tol=1e-6, neighbours=4):
    """
    This function imposes boundary conditions coming from a DVC result to the nodes of an unstructured FE mesh.

    Parameters
    ----------
        meshNodes: 2D numpy array
            Array of ``n`` node positions of the unstructured mesh
            Each line is [nodeNumber, z, y, x]

        dvcField: 2D numpy array
            Array of ``m`` points of the dvc field
            Each line is [zPos, yPos, xPos, zDisp, yDisp, xDisp]

        mask: 2D numpy array, optional
            Boolean array of ``m`` points of the dvc field
            Points with 0 will be ignored for the field interpolation
            Default = None (`i.e.` interpolate based on all of the dvc points)

        pixelSize: float, optional
            physical size of a pixel (`i.e.` 1mm/px)
            Default = 1.0

        meshType: string, optional
            For the moment, valid inputs are ``cube`` and ``cylinder``
            The axis of a cylinder is considered to be ``z``
            Note that if a cylindrical mesh is passed, ``centre`` and ``radius`` are highly recommended
            Default = `cube`

        centre: float, optional
            The centre of the cylinder [y, x] in physical units (`i.e.` mm)
            Default = [0, 0]

        radius: float, optional
            The radius of the cylinder in physical units (`i.e.` mm)
            Default = 1.0

        topBottom: bool, optional
            If boundary conditions are passed only for the top (`i.e.` z=zmax)  and bottom (`i.e.` z=zmin) surfaces of the mesh
            Default = False

        tol: float, optional
            Numerical tolerance for floats equality
            Default = 1e-6

        neighbours: int, , optional
            Neighbours for field interpolation
            Default = 4
    Returns
    -------
        bc: 2D numpy array
            Boundary node displacements
            Each line is [nodeNumber, zPos, yPos, xPos, zDisp, yDisp, xDisp]

    WARNING
    -------
        1. All coordinates and displacement arrays are ``z``, ``y``, ``x``
        2. The axis of a cylinder is considered to be ``z``
    """
    import numpy
    from scipy.spatial import KDTree

    # STEP 1: find the edge nodes
    posMax = [meshNodes[:, i].max() for i in range(1, 4)]
    posMin = [meshNodes[:, i].min() for i in range(1, 4)]
    bcNodes = []

    if meshType == "cube":
        # extract edge nodes from the mesh
        for node in meshNodes:
            if topBottom:
                testMin = abs(node[1] - posMin[0]) < tol
                testMax = abs(node[1] - posMax[0]) < tol
            else:
                testMin = abs(node[1] - posMin[0]) < tol or abs(node[2] - posMin[1]) < tol or abs(node[3] - posMin[2]) < tol
                testMax = abs(node[1] - posMax[0]) < tol or abs(node[2] - posMax[1]) < tol or abs(node[3] - posMax[2]) < tol
            if testMin or testMax:
                bcNodes.append(node)
    elif meshType == "cylinder":
        # extract edge nodes from the mesh
        for node in meshNodes:
            testZ = abs(node[1] - posMin[0]) < tol or abs(node[1] - posMax[0]) < tol
            testXY = False
            if not topBottom:
                testXY = (node[2] - centre[0])**2 + (node[3] - centre[1])**2 >= (radius - tol)**2
            if testZ or testXY:
                bcNodes.append(node)

    bcNodes = numpy.array(bcNodes)
    m = bcNodes.shape[0]

    # STEP 2: convert dvc field to physical unit
    dvcField *= pixelSize

    # STEP 3: Interpolate the disp values of FE using a weighted influence of the k nearest neighbours from DVC coord
    bcDisp = numpy.zeros((m, 3))
    # create the k-d tree of the coordinates of DVC good points
    if mask is None:
        mask = numpy.ones(dvcField.shape[0])

    goodPoints = numpy.where(mask == 1)
    treeCoord = KDTree(dvcField[:, :3][goodPoints])

    for node in range(m):
        distance, ind = treeCoord.query(bcNodes[node, 1:], k=neighbours)

        # Check if we've hit the same point
        if numpy.any(distance == 0):
            bcDisp[node, 0] = dvcField[goodPoints][ind][numpy.where(distance == 0)][0, 3]
            bcDisp[node, 1] = dvcField[goodPoints][ind][numpy.where(distance == 0)][0, 4]
            bcDisp[node, 2] = dvcField[goodPoints][ind][numpy.where(distance == 0)][0, 5]

        else:
            weightSumInv = sum(1 / distance)
            # loop over neighbours
            for neighbour in range(neighbours):
                # calculate its weight
                weightInv = (1 / distance[neighbour]) / float(weightSumInv)
                # replace the disp values the weighted disp components of the ith nearest neighbour
                bcDisp[node, 0] += dvcField[goodPoints][ind[neighbour], 3] * weightInv
                bcDisp[node, 1] += dvcField[goodPoints][ind[neighbour], 4] * weightInv
                bcDisp[node, 2] += dvcField[goodPoints][ind[neighbour], 5] * weightInv

    # return node number and displacements
    return numpy.hstack((bcNodes, bcDisp))


def tetVolumes(coordinates, connectivity):
    """
    This function computes volumes of the tetrahedra passed with a connectivity matrix.
    Using algorithm in https://en.wikipedia.org/wiki/Tetrahedron#Volume

    Parameters
    ----------
        coordinates : Nx3 array
            Array of ``N`` coordinates of the nodes

        connectivity : Mx4 array
            Array of ``M`` none numbers that are connected as tetrahedra (e.g., the output from triangulate)

    Returns
    -------
        volumes : vector of length M
            Volumes of tetrahedra

    Note
    -----
        Pure python function.
    """
    import numpy
    # Sanity checks on lengths:
    if connectivity.shape[1] != 4 or coordinates.shape[1] != 3 or connectivity.max() > coordinates.shape[0]:
        print("spam.mesh.tetVolumes(): Dimensionality problem, not running")
        print("connectivity.max()", connectivity.max(), "coordinates.shape[0]", coordinates.shape[0])
        return

    volumes = numpy.zeros(connectivity.shape[0], dtype='<f4')
    connectivity = connectivity.astype(numpy.uint)

    # loop through tetrahedra
    for tetNumber in range(connectivity.shape[0]):
        fourNodes = connectivity[tetNumber]
        a = coordinates[fourNodes[0]]
        b = coordinates[fourNodes[1]]
        c = coordinates[fourNodes[2]]
        d = coordinates[fourNodes[3]]
        volumes[tetNumber] = numpy.abs(numpy.dot((a - d), numpy.cross((b - d), (c - d)))) / 6.0

    return volumes
