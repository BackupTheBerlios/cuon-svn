import os
import re
from copy import deepcopy

class src2dia:
    def __init__(self,name="cuon1",height=600,width=800):
        self.name = name
        self.items = []
        self.height = height
        self.width = width
        self.style = 'fill-opacity:1.0'
        self.stroke = 'blue'
        self.stroke_width = 2
        self.rClass = re.compile('^class ')
        self.rBrackets = re.compile('.*\(.*\)')
        self.rBracketsOn = re.compile('.*\(')
        self.rBracketsOff = re.compile('.*\)')
        self.rDef = re.compile('^def ')
    
    def add(self,item): 
        self.items.append(item)

    
    def getXml(self):
        var = []
        for item in self.items: 
            var += item.getXml()            
        
        return var

    def write_dia(self,filename=None):
        if filename:
            self.dianame = filename
        else:
            self.dianame = self.name + ".dia"
        file = open(self.dianame,'w')
        file.writelines(self.getXml())
        file.close()
        return

    def display(self,prog='/usr/bin/dia'):
        os.system("%s %s" % (prog,self.dianame))
        return        
        
class Header:
    def __init__(self):
        pass
    def getXml(self):
        s = '<?xml version="1.0" encoding="UTF-8"?> \n \
                <dia:diagram xmlns:dia="http://www.lysator.liu.se/~alla/dia/"> \n \
                      <dia:diagramdata> \n \
                        <dia:attribute name="background"> \n \
                          <dia:color val="#ffffff"/> \n \
                        </dia:attribute> \n \
                        <dia:attribute name="pagebreak"> \n \
                          <dia:color val="#000099"/> \n \
                        </dia:attribute> \n \
                        <dia:attribute name="paper"> \n \
                          <dia:composite type="paper"> \n \
                            <dia:attribute name="name"> \n \
                              <dia:string>#A4#</dia:string> \n \
                            </dia:attribute> \n \
                            <dia:attribute name="tmargin"> \n \
                              <dia:real val="2.8222000598907471"/> \n \
                            </dia:attribute> \n \
                            <dia:attribute name="bmargin"> \n \
                              <dia:real val="2.8222000598907471"/> \n \
                            </dia:attribute> \n \
                            <dia:attribute name="lmargin"> \n \
                              <dia:real val="2.8222000598907471"/> \n \
                            </dia:attribute> \n \
                            <dia:attribute name="rmargin"> \n \
                              <dia:real val="2.8222000598907471"/> \n \
                            </dia:attribute> \n \
                            <dia:attribute name="is_portrait"> \n \
                              <dia:boolean val="true"/> \n \
                            </dia:attribute> \n \
                            <dia:attribute name="scaling"> \n \
                              <dia:real val="1"/> \n \
                            </dia:attribute> \n \
                            <dia:attribute name="fitto"> \n \
                              <dia:boolean val="false"/> \n \
                            </dia:attribute> \n \
                          </dia:composite> \n \
                        </dia:attribute> \n \
                        <dia:attribute name="grid"> \n \
                          <dia:composite type="grid"> \n \
                            <dia:attribute name="width_x"> \n \
                              <dia:real val="1"/> \n \
                            </dia:attribute> \n \
                            <dia:attribute name="width_y"> \n \
                              <dia:real val="1"/> \n \
                            </dia:attribute> \n \
                            <dia:attribute name="visible_x"> \n \
                              <dia:int val="1"/> \n \
                            </dia:attribute> \n \
                            <dia:attribute name="visible_y"> \n \
                              <dia:int val="1"/> \n \
                            </dia:attribute> \n \
                            <dia:composite type="color"/> \n \
                          </dia:composite> \n \
                        </dia:attribute> \n \
                        <dia:attribute name="color"> \n \
                          <dia:color val="#d8e5e5"/> \n \
                        </dia:attribute> \n \
                        <dia:attribute name="guides"> \n \
                          <dia:composite type="guides"> \n \
                            <dia:attribute name="hguides"/> \n \
                            <dia:attribute name="vguides"/> \n \
                          </dia:composite> \n \
                        </dia:attribute> \n \
                      </dia:diagramdata> \n \
                      <dia:layer name="Background" visible="true"> \n' 
                          
        return s
      
        
class Footer:
    def __init__(self):
        pass
    def getXml(self):    
        s = '  </dia:layer> \n \
                </dia:diagram> \n'
        return s

class startObject:
    def __init__(self):
        self.classname = None

    def getXml(self):    
        s = '           <dia:object type="UML - Class" version="0" id="O0">  \n \
              <dia:attribute name="obj_pos">  \n \
                <dia:point val="50.0,50.0"/>  \n \
              </dia:attribute>  \n \
              <dia:attribute name="obj_bb">  \n \
                <dia:rectangle val="50.0,50.0;50.0,50.0"/>  \n \
              </dia:attribute>  \n \
              <dia:attribute name="elem_corner">  \n \
                <dia:point val="40.0,40.0"/>  \n \
              </dia:attribute>  \n \
              <dia:attribute name="elem_width">  \n \
                <dia:real val="1.0"/>  \n \
              </dia:attribute>  \n \
              <dia:attribute name="elem_height">  \n \
                <dia:real val="1.0"/>  \n \
              </dia:attribute>  \n \
              <dia:attribute name="name">  \n \
                <dia:string>#%s#</dia:string>  \n \
              </dia:attribute>  \n \
              <dia:attribute name="stereotype">  \n \
                <dia:string/>  \n \
              </dia:attribute>  \n \
              <dia:attribute name="abstract">  \n \
                <dia:boolean val="false"/>  \n \
              </dia:attribute>  \n \
              <dia:attribute name="suppress_attributes">  \n \
                <dia:boolean val="false"/>  \n \
              </dia:attribute>  \n \
              <dia:attribute name="suppress_operations">  \n \
                <dia:boolean val="false"/>  \n \
              </dia:attribute>  \n \
              <dia:attribute name="visible_attributes">  \n \
                <dia:boolean val="true"/>  \n \
              </dia:attribute>  \n \
              <dia:attribute name="visible_operations">  \n \
                <dia:boolean val="true"/>  \n \
              </dia:attribute>  \n \
              <dia:attribute name="foreground_color"> \n \
                <dia:color val="#000000"/>  \n \
              </dia:attribute>  \n \
              <dia:attribute name="background_color">  \n \
                <dia:color val="#ffffff"/>  \n \
              </dia:attribute>  \n \
              <dia:attribute name="normal_font">  \n \
                <dia:font name="Courier"/>  \n \
              </dia:attribute>  \n \
              <dia:attribute name="abstract_font">  \n \
                <dia:font name="Courier-Oblique"/>  \n \
              </dia:attribute>  \n \
              <dia:attribute name="classname_font">  \n \
                <dia:font name="Helvetica-Bold"/>  \n \
              </dia:attribute>  \n \
              <dia:attribute name="abstract_classname_font">  \n \
                <dia:font name="Helvetica-BoldOblique"/>  \n \
              </dia:attribute>  \n \
              <dia:attribute name="font_height">  \n \
                <dia:real val="0.8"/>  \n \
              </dia:attribute>  \n \
              <dia:attribute name="abstract_font_height">  \n \
                <dia:real val="0.8"/>  \n \
              </dia:attribute>  \n \
              <dia:attribute name="classname_font_height">  \n \
                <dia:real val="1"/>  \n \
              </dia:attribute>  \n \
              <dia:attribute name="abstract_classname_font_height">  \n \
                <dia:real val="1"/>  \n \
              </dia:attribute>  \n \
              <dia:attribute name="template">  \n \
                <dia:boolean val="false"/>  \n \
              </dia:attribute>  \n ' %self.classname
        return s
        
class endObject:
    def __init__(self):
        pass
    def getXml(self):    
        s = ' </dia:object> \n '
        return s
        
class startOperations:
    def __init__(self):
        pass
    def getXml(self):    
        s = '  <dia:attribute name="operations"> \n '
        return s
class endOperations:
    def __init__(self):
        pass
    def getXml(self):    
        s = '  </dia:attribute> \n '
        return s        

class startUMLOperation:
    def __init__(self):
        self.defname = None
        
    def getXml(self):    
        s = '  <dia:composite type="umloperation">  \n \
          <dia:attribute name="name">  \n \
            <dia:string>#%s#</dia:string>  \n \
          </dia:attribute>  \n \
          <dia:attribute name="stereotype">  \n \
            <dia:string/>  \n \
          </dia:attribute>  \n \
          <dia:attribute name="type">  \n \
            <dia:string>##</dia:string>  \n \
          </dia:attribute>  \n \
          <dia:attribute name="visibility">  \n \
            <dia:enum val="0"/>  \n \
          </dia:attribute>  \n \
          <dia:attribute name="abstract">  \n \
            <dia:boolean val="false"/>  \n \
          </dia:attribute>  \n \
          <dia:attribute name="inheritance_type">  \n \
            <dia:enum val="1"/>  \n \
          </dia:attribute>  \n \
          <dia:attribute name="query">  \n \
            <dia:boolean val="false"/>  \n \
          </dia:attribute>  \n \
          <dia:attribute name="class_scope">  \n \
            <dia:boolean val="false"/>  \n \
          </dia:attribute>  \n ' %self.defname
        return s
        
class endUMLOperation:
    def __init__(self):
        pass
    def getXml(self):         
        s = '</dia:composite> \n'
        return s
class startParameters:
    def __init__(self):
        pass
    def getXml(self):         
        s = '<dia:attribute name="parameters"> \n '
        return s
        
class parameters:
    def __init__(self):
        self.paraname = None
    def getXml(self):         
        s = ' <dia:composite type="umlparameter"> \n \
              <dia:attribute name="name"> \n \
                <dia:string>#%s#</dia:string> \n \
              </dia:attribute> \n \
              <dia:attribute name="type"> \n \
                <dia:string>##</dia:string> \n \
              </dia:attribute> \n \
              <dia:attribute name="value"> \n \
                <dia:string/> \n \
              </dia:attribute> \n \
              <dia:attribute name="kind"> \n \
                <dia:enum val="0"/> \n \
              </dia:attribute> \n \
            </dia:composite> \n ' %self.paraname

        return s
        
class endParameters:
    def __init__(self):
        pass
    def getXml(self):         
        s = '</dia:attribute> \n '
        return s
              
def colorstr(rgb): 
    return "#%x%x%x" % (rgb[0]/16,rgb[1]/16,rgb[2]/16)

def getParameter(dia, m,sLine):
    print '====================================='
    print m
    print sLine, m.end()
    print sLine[m.end():]
    m2 = dia.rBracketsOn.match(sLine)
    if m2:
        print 'm2', sLine[m.end():m2.end()-1]
        opname = sLine[m.end():m2.end()-1]
            
        m3 = dia.rBracketsOff.match(sLine)
        if m3:
            print sLine
            print m2.start(), m2.end()
            print m3.start(), m3.end()
            
            print 'm3', sLine[m2.end():m3.end()-1]
            liPara = sLine[m2.end():m3.end()-1]
    print 'opname', opname
    liPara = liPara.split(',')
    for i in range(len(liPara)):
        liPara[i] = liPara[i].strip()
    print 'liPara', liPara
    print '****************************************'
    
    
    return opname,liPara
        
def start():
    filenames = ['./CUON/Cuon.py']
    
    
    dia = src2dia('cuon')
    
    dia.add(Header())
 
    for fName in filenames:
        f = open(fName,'r')
        sLine = f.readline()
        sO = startObject()
        sD = startUMLOperation()
        sP = parameters()
        while sLine:
            sLine = sLine.strip()
            m = dia.rClass.match(sLine)
            if m:
                sO.classname, liInherits = getParameter(dia, m,sLine)
                print '#####################'
                print sO.classname
                print liInherits
                dia.add(deepcopy(sO))
                dia.add(startOperations())
            m = dia.rDef.match(sLine)
            if m:
                print m.end()
                print sLine
                s1,li1 = getParameter(dia, m,sLine)
                print '++++++++++++++++++++++++++'
                print s1
                print li1
                sD.defname = s1
                dia.add(deepcopy(sD))
                dia.add(startParameters())
                for i in li1:
                    print 'paraname', i
                    sP.paraname = i
                    dia.add(deepcopy(sP))
                dia.add(endParameters())
                dia.add(endUMLOperation())
                
            sLine = f.readline()
            
    
    
#        dia.add(parameters())
#        dia.add(parameters())
        
            
        
        
        dia.add(endOperations())
    
    
        dia.add(endObject())
    dia.add(Footer())
    
    dia.write_dia()
    
    return

if __name__ == '__main__': 
    start()

\
