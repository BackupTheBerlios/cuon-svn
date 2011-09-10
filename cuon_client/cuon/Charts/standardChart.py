# coding=utf-8
##Copyright (C) [2011]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 

try:
    import numpy as np
    import matplotlib.pyplot as plt
    runChart = True
except ImportError:
    print "Please install numpy and matplotlib"
    runChart = False

class chart():
    def __init__(self):
    

        self.charts = ['barchart', 'circle']
        self.runChart = runChart
        self.N=5
        self.liX=[]
        self.liY = []
        self.width = 0.35
        self.ind = None
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.chartType = 0
        self.yLabel = None
        self.xLabel = None
        self.Title = None
        self.xTickLabels = None
        self.yTickLabels = None
        self.liLegend = None
        
    def setN(self, n):
        self.N = n
        self.newRange()
        
    def addX(self, liX):
        self.liX.append(liX)
        
    def addY(self, liY):
        self.liY.append(liY)
        
    def setWidth(self, w):
        self.width = w
        
    def newRange(self):
        self.ind =  np.arange(self.N)  # the x locations for the groups
        
    def setChartType(self, iType):
        self.chartType = iType
        
    def setXLabel(self, s):
        self.xLabel = s
    def setYLabel(self, s):
        self.yLabel = s
        
    def setXTickLabels(self, liS):
        self.xTickLabels = liS
    def setYTickLabels(self, liS):
        self.yTickLabels = liS   
        
    def setTitle(self, s):
        self.Title = s
        
    def setLegend(self, liS):
        self.liLegend = liS
    def autolabel(self, rects):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            self.ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),ha='center', va='bottom')
            
            
    def start(self):
        if self.runChart:
            if self.chartType == 0:
                if len(liX)== 2:
                    self.rects1 = self.ax.bar(self.ind, self.liX[0], self.width, color='r', yerr=self.liX[1])
                elif  len(liX)== 1:
                    self.rects1 = self.ax.bar(self.ind, self.liX[0], self.width, color='r')
                
                if len(liY)== 2:
                    self.rects2 = self.ax.bar(self.ind+self.width, self.liY[0], self.width, color='y', yerr=self.liY[1])
                elif len(liY)== 1:
                    self.rects2 = self.ax.bar(self.ind+self.width, self.liY[0], self.width, color='y')
                
                # add some
                if self.yLabel:
                    self.ax.set_ylabel(self.yLabel)
                if self.xLabel:
                    self.ax.set_xlabel(self.yLabel)
                if self.Title:
                    self.ax.set_title(self.Title)
                if self.xTickLabels:
                    self.ax.set_xticks(self.ind+self.width)
                    self.ax.set_xticklabels( self.xTickLabels )
        
                if self.liLegend:
                    self.ax.legend( (self.rects1[0], self.rects2[0]), self.liLegend )
                self.autolabel(self.rects1)
                self.autolabel(self.rects2)
                
                self.show()
                
        

    def show(self):
      

        plt.show()
#        
#ch = chart()
#ch.setN(5)
#ch.addX([20, 35, 30, 35, 27])
#ch.addX   ([2, 3, 4, 1, 2])
#        
#ch.addY ([25, 32, 34, 20, 25])
#ch.addY ([3, 5, 2, 3, 3])
#        
#ch.setTitle('MyTitle')
#
#ch.start()
