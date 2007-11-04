import os

class SVG:
    def __init__(self):
        pass
        
    

    def BarChart(self,dicScene, liValue):
            
        
            
            scene = newSVG(dicScene['title'],dicScene['height'],dicScene['width'])
            
            scene.add(Rectangle((10,10),dicScene['height'] - dicScene['yMargin'],dicScene['width']- dicScene['xMargin'],dicScene['colorFill']))
            scene.add(Line((dicScene['xMargin'] + 10,dicScene['yMargin'] + 10),(dicScene['xMargin'] + 10,dicScene['height'] - dicScene['yMargin'] -30)))
            scene.add(Line((dicScene['xMargin'] + 10,dicScene['height'] - dicScene['yMargin'] -30),(dicScene['width'] - dicScene['xMargin'] -10,dicScene['height'] - dicScene['yMargin'] -30)))
    
            iCounter = len(liValue)
            xRange = int( (dicScene['width'] - dicScene['xMargin'] -20)/iCounter) -1
            #xRange = xRange - 5
            print xRange
            liMax = []
            for iT in liValue:
                print iT
                liMax.append(iT[1])
            yM = max(liMax)
            if yM == 0:
                yM = 1
            
            yMulti0 = ( (dicScene['height'] - dicScene['yMargin'] -30)/yM)*0.9
            yMulti = int(yMulti0)
            if yMulti <= 1:
                yMulti = 1
                yMulti0 = 1
                
            print 'yMultis'
            print yM, yMulti
            yCounter = int( (dicScene['height'] - dicScene['yMargin'] -30)/10)
            # create legend
            for yTextPos in range(0,10):
                #print 'TextPos.:', yTextPos
                #print (int( dicScene['xMargin']-10 ),int(dicScene['height'] - dicScene['yMargin'] - yCounter*yMulti)*yTextPos)
                #print `yTextPos*yMulti`
                #print dicScene['height'] - dicScene['xMargin']
                #print yCounter,yMulti
                scene.add(Text( (int( dicScene['xMargin']-20 ),int(dicScene['height'] - dicScene['yMargin'] -30 - yCounter*yTextPos)),`yTextPos*yCounter/yMulti`,dicScene['yFontSize']))
            for x in range(0,iCounter):
                x1 = xRange*x + dicScene['xMargin'] + 10 ,dicScene['height'] - dicScene['yMargin'] -30
                
                #y1 = (liValue[x], xRange)
                y1 = (int(-(liValue[x][1])*yMulti),int(xRange/2 -2))
                
                print x1, y1
                scene.add(Rectangle(x1,y1[0],y1[1],(dicScene['Axis']['colorFill'])))
                #print (int(x1),int(yM + 10)),`liValue[x][0]`,14
                scene.add(Text((x1[0],int(x1[1] + dicScene['xFontSize'])),`liValue[x][0]`,dicScene['xFontSize']))
            self.endChart(scene)
        
    def endChart(self, scene):
        scene.write_svg()
        #scene.display()
    
    def display(self,prog='/usr/bin/eog'):
        os.system("%s %s" % (prog,self.svgname))
        return        
        

class newSVG:
    def __init__(self,name="svg",height=600,width=800):
        self.name = name
        self.items = []
        self.height = height
        self.width = width
        self.style = 'fill-opacity:1.0'
        self.stroke = 'blue'
        self.stroke_width = 2
    def add(self,item): 
        self.items.append(item)

    def getXml(self):
        var = ['<?xml version="1.0" standalone="no" ?>\n <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN" \n   "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd"> \n ',
               '<svg height=\"%d\" width=\"%d\"  xmlns="http://www.w3.org/2000/svg"  xmlns:xlink="http://www.w3.org/1999/xlink" > \n ' % (self.height,self.width),
               ' <g style=\"%s; stroke:%s;\n' %(self.style,self.stroke),
               '  stroke-width:%i;\">\n' %(self.stroke_width)]
        for item in self.items: 
            var += item.getXml()            
        var += [" </g>\n</svg>\n"]
        return var
        
    def write_svg(self,filename=None):
        if filename:
            self.svgname = filename
        else:
            self.svgname = self.name + ".svg"
        file = open(self.svgname,'w')
        file.writelines(self.getXml())
        file.close()
        return
        
class Line:
    def __init__(self,start,end):
        self.start = start #xy tuple
        self.end = end     #xy tuple
        return

    def getXml(self):
        return ["  <line x1=\"%d\" y1=\"%d\" x2=\"%d\" y2=\"%d\" />\n" %\
                (self.start[0],self.start[1],self.end[0],self.end[1])]


class Circle:
    def __init__(self,center,radius,color):
        self.center = center #xy tuple
        self.radius = radius #xy tuple
        self.color = color   #rgb tuple in range(0,256)
        return

    def getXml(self):
        return ["  <circle cx=\"%d\" cy=\"%d\" r=\"%d\"\n" %\
                (self.center[0],self.center[1],self.radius),
                "    style=\"fill:%s;\"  />\n" % colorstr(self.color)]

class Rectangle:
    def __init__(self,origin,height,width,color):
        self.origin = origin
        self.height = height
        self.width = width
        self.color = color
        return

    def getXml(self):
        return ["  <rect x=\"%d\" y=\"%d\" height=\"%d\"\n" %\
                (self.origin[0],self.origin[1],self.height),
                "    width=\"%d\" style=\"fill:%s;\" />\n" %\
                (self.width,colorstr(self.color))]

class Text:
    def __init__(self,origin,text,size=24):
        self.origin = origin
        self.text = text
        self.size = size
        return

    def getXml(self):
        print 'Text'
        print self.origin
        print self.size
        print self.text
        return ["  <text x=\"%d\" y=\"%d\" font-size=\"%d\">\n" %\
                (self.origin[0],self.origin[1],self.size),
                "   %s\n" % self.text,
                "  </text>\n"]
        
    
def colorstr(rgb): 
    return "#%x%x%x" % (rgb[0]/16,rgb[1]/16,rgb[2]/16)



        
    
####def test():
####    scene = SVG('test')
####    scene.add(Rectangle((100,100),200,200,(0,255,255)))
####    scene.add(Line((200,200),(200,300)))
####    scene.add(Line((200,200),(300,200)))
####    scene.add(Line((200,200),(100,200)))
####    scene.add(Line((200,200),(200,100)))
####    scene.add(Circle((200,200),30,(0,0,255)))
####    scene.add(Circle((200,300),30,(0,255,0)))
####    scene.add(Circle((300,200),30,(255,0,0)))
####    scene.add(Circle((100,200),30,(255,255,0)))
####    scene.add(Circle((200,100),30,(255,0,255)))
####    scene.add(Text((50,50),"Testing SVG"))
####    
####    #scene.write_svg()
####    #scene.display()
####    
####    
####    dicScene = {}
####    dicScene['title'] = 'BarChart'
####    dicScene['height'] = 550
####    dicScene['width'] = 450
####    dicScene['xMargin'] = 20
####    dicScene['yMargin'] = 20
####    dicScene['colorMargin'] = (122,25,215)
####
####    dicScene['Axis'] = {}    
####    dicScene['Axis']['xAxisMargin'] = 20
####    dicScene['Axis']['yAxisMargin'] = 20
####    dicScene['Axis']['colorMargin'] = (222,125,15)
####    dicScene['Axis']['colorTextFG'] = (222,125,15)
####    dicScene['Axis']['colorTextBG'] = (225,225,215)
####
####    
####    t1 = SVG()
####    t1.BarChart(dicScene,[(1,60),(1,120),(1,40),(1,90),(1,120)])
####    
####    return
####
####if __name__ == '__main__': 
####    test()

