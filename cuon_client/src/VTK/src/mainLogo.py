# -*- coding: utf-8 -*-

##Copyright (C) [2003]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 


import vtk
import time

# 
# Next we create an instance of vtkConeSource and set some of its
# properties. The instance of vtkConeSource "cone" is part of a visualization
# pipeline (it is a source process object); it produces data (output type is
# vtkPolyData) which other filters may process.
#

class mainLogo:

    def __init__(self):
        cone = vtk.vtkConeSource()
        cone.SetHeight( 3.0 )
        cone.SetRadius( 1.0 )
        cone.SetResolution( 10 )

        
        # 
        # In this example we terminate the pipeline with a mapper process object.
        # (Intermediate filters such as vtkShrinkPolyData could be inserted in
        # between the source and the mapper.)  We create an instance of
        # vtkPolyDataMapper to map the polygonal data into graphics primitives. We
        # connect the output of the cone souece to the input of this mapper.
        #
        coneMapper = vtk.vtkPolyDataMapper()
        coneMapper.SetInput(cone.GetOutput())

        # 
        # Create an actor to represent the cone. The actor orchestrates rendering of
        # the mapper's graphics primitives. An actor also refers to properties via a
        # vtkProperty instance, and includes an internal transformation matrix. We
        # set this actor's mapper to be coneMapper which we created above.
        #
        self.coneActor = vtk.vtkActor()
        self.coneActor.SetMapper(coneMapper)
        self.ren1 = None
        self.ren2 = None
        self.renWin = None
        

    def createRenderer(self):
        # 
        # Create two renderers and assign actors to them. A renderer renders into a
        # viewport within the vtkRenderWindow. It is part or all of a window on the
        # screen and it is responsible for drawing the actors it has.  We also set
        # the background color here. In this example we are adding the same actor
        # to two different renderers; it is okay to add different actors to
        # different renderers as well.
        #
        self.ren1 = vtk.vtkRenderer()
        self.ren1.AddActor(self.coneActor)
        self.ren1.SetBackground(0.1, 0.2, 0.4)
        self.ren1.SetViewport(0.0, 0.0, 0.5, 1.0)

        self.ren2 = vtk.vtkRenderer()
        self.ren2.AddActor(self.coneActor)
        self.ren2.SetBackground(0.1, 0.2, 0.4)
        self.ren2.SetViewport(0.5, 0.0, 1.0, 1.0)


    def createWin(self):
        #
        # Finally we create the render window which will show up on the screen.
        # We add our two renderers into the render window using AddRenderer. We also
        # set the size to be 600 pixels by 300.
        #
        self.renWin = vtk.vtkRenderWindow()
        self.renWin.AddRenderer( self.ren1 )
        self.renWin.AddRenderer( self.ren2 )
        self.renWin.SetSize(600, 300)
        #self.renWin.set_title('C.U.O.N. Linux and Business')
        #
        # Make one camera view 90 degrees from other.
        #
        self.ren1.GetActiveCamera().Azimuth(90)

   
    def startMainloop(self):
        #
        # Now we loop over 360 degreeees and render the cone each time.
        #

        for i in range(0,60):
            time.sleep(0.03)
            
            self.renWin.Render()
            self.ren1.GetActiveCamera().Azimuth( 1 )
            self.ren2.GetActiveCamera().Azimuth( 1 )


    def startLogo(self):
        self.createRenderer()
        self.createWin()
        self.startMainloop()
        
