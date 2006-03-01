import sys
sys.path.append('/usr/lib/python/')
sys.path.append('/usr/lib/python/site-packages/Numeric')

# generate the data.
from Numeric import *
#import mayavi
import time
#import pyvtk
#import vtk
import os

class test:
    def __init__(self):
        pass
        
        #x = (arange(50.0)-25)/2.0
        #y = (arange(50.0)-25)/2.0
        #r = sqrt(x[:,NewAxis]**2+y**2)
        #z = 1.2*r
        # now dump the data to a VTK file.
        # Flatten the 2D array data as per VTK's requirements.
        x= resize(array((2,3,4,5,6,7,8,9)), (29,29))
        y=array((1,2,3,4,5,6,7,8))
        a=array((1,2,1,2,1,2,1,2))
        #z = x*y*a
        z1 = reshape(transpose(x), (-1,))
        point_data = pyvtk.PointData(pyvtk.Scalars(z1))
        grid = pyvtk.StructuredPoints((29,29,1), (1, 1, 1), (2, 2, 2))
        data = pyvtk.VtkData(grid, point_data)
        data.tofile('/tmp/test.vtk')
        
    def show2(self):
         np = 21
         tmin, tmax = 0. , 2*N.pi
         dt = (tmax-tmin)/float(np-1)
         # parametric representation
         t = tmin + dt*N.arange(0, np)
         x = N.cos(2*t)
         y = N.sin(2*t)
         z = t/(2*N.pi)
         # store in Numeric array
         xyz = N.zeros( (np, 3), N.Float64 )
         xyz[:,0] = x; xyz[:,1] = y; xyz[:,2] = z;

         # create vtk array and pass Num array pointer to it
         vtk_array = vtk.vtkDoubleArray()
         vtk_array.SetNumberOfTuples(np)
         vtk_array.SetNumberOfComponents(3)
         vtk_array.SetVoidArray(xyz.flat, 3*np, 1)


         # create vtk Point object
         polyLinePoints = vtk.vtkPoints()
         polyLinePoints.SetNumberOfPoints(np)
         polyLinePoints.SetData(vtk_array)

         # create PolyLine object
         aPolyLine = vtk.vtkPolyLine()
         aPolyLine.GetPointIds().SetNumberOfIds(np)
         # set the id numbers (can one do without the for loop?)
         for i in range(np):
             aPolyLine.GetPointIds().SetId(i, i)
         aPolyLineGrid = vtk.vtkUnstructuredGrid()
         aPolyLineGrid.Allocate(1, 1)
         aPolyLineGrid.InsertNextCell(aPolyLine.GetCellType(),
                                      aPolyLine.GetPointIds())
         aPolyLineGrid.SetPoints(polyLinePoints)
         aPolyLineMapper = vtk.vtkDataSetMapper()
         aPolyLineMapper.SetInput(aPolyLineGrid)
         aPolyLineActor = vtk.vtkActor()
         aPolyLineActor.SetMapper(aPolyLineMapper)
         aPolyLineActor.AddPosition(2, 0, 4)
         aPolyLineActor.GetProperty().SetDiffuseColor(1, 1, 1)


         ren = vtk.vtkRenderer()
         renWin = vtk.vtkRenderWindow()
         renWin.AddRenderer(ren)
         renWin.SetSize(500, 400)
         iren = vtk.vtkRenderWindowInteractor()
         iren.SetRenderWindow(renWin)

         ren.SetBackground(.1, .2, .4)

         ren.AddActor(aPolyLineActor)

         ren.GetActiveCamera().Azimuth(30)
         ren.GetActiveCamera().Elevation(20)
         ren.ResetCameraClippingRange()

         # Render the scene and start interaction.
         iren.Initialize()
         renWin.Render()
         iren.Start()


    def show3(self):
        v = mayavi.mayavi() # create a MayaVi window.
        dir(v)
        d = v.open_vtk('/tmp/test.vtk', config=1) # open the data file.
        # The config option turns on/off showing a GUI control for the data/filter/module.
        # load the filters.
        f = v.load_filter('WarpScalar', config=0) 
        n = v.load_filter('PolyDataNormals', 0)
        n.fil.SetFeatureAngle (45) # configure the normals.
        # Load the necessary modules.
        m = v.load_module('SurfaceMap', 0)
        a = v.load_module('Axes', 0)
        a.axes.SetCornerOffset(0.0) # configure the axes module.
        o = v.load_module('Outline', 0)
        v.Render() # Re-render the scene.
        v.master.wait_window()
        # Line coordinate points

    def show(self):
          data = ' -d /tmp/test.vtk '
          mod  = ' -m Axes -m SurfaceMap '
          filter = ' -f WarpScalar -f PolyDataNormals'
          os.system('mayavi  ' + data + mod + filter  + ' &')
