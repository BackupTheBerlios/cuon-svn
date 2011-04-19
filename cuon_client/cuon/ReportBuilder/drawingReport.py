

import pygtk
pygtk.require('2.0')
import gtk
import operator
import time
import string
from cuon.Windows.gladeXml import gladeXml


class drawingReport(gladeXml):
    def __init__(self):
        gladeXml.__init__(self)
        self.area = None
        self.pangolayout = None
        self.sw = None
        self.table = None
        
        self.hruler = None
        self.vruler = None
        
        self.drawObjects = []
        
        self.table = gtk.Table(2,2)
        self.hruler = gtk.HRuler()
        self.vruler = gtk.VRuler()
        self.Zoom = 2
        
    def createDA(self, sw, vp, da,  width,  height):
        self.area = da
        self.sw = sw
        
        self.area.set_size_request(width*self.Zoom,  height*self.Zoom)
        self.pangolayout = self.area.create_pango_layout("")
        self.hruler.set_range(0, width*self.Zoom, 0, width*self.Zoom)
        self.vruler.set_range(0, height*self.Zoom,  0, height*self.Zoom)
        self.table.attach(self.hruler, 1, 2, 0, 1, yoptions=0)
        self.table.attach(self.vruler, 0, 1, 1, 2, xoptions=0)
        self.table.attach(self.sw, 1, 2, 1, 2)
        self.sw.add(self.table)
        self.area.set_events(gtk.gdk.POINTER_MOTION_MASK |
                             gtk.gdk.POINTER_MOTION_HINT_MASK )
        self.area.connect("expose-event", self.area_expose_cb)
        
        
        def motion_notify(ruler, event):
            return ruler.emit("motion_notify_event", event)
        self.area.connect_object("motion_notify_event", motion_notify,
                                 self.hruler)
        self.area.connect_object("motion_notify_event", motion_notify,
                                 self.vruler)
        self.hadj = self.sw.get_hadjustment()
        self.vadj = self.sw.get_vadjustment()
        def val_cb(adj, ruler, horiz):
            if horiz:
                span = self.sw.get_allocation()[3]
            else:
                span = self.sw.get_allocation()[2]
            l,u,p,m = ruler.get_range()
            v = adj.value
            ruler.set_range(v, v+span, p, m)
            while gtk.events_pending():
                gtk.main_iteration()
        self.hadj.connect('value-changed', val_cb, self.hruler, True)
        self.vadj.connect('value-changed', val_cb, self.vruler, False)
        def size_allocate_cb(wid, allocation):
            x, y, w, h = allocation
            l,u,p,m = self.hruler.get_range()
            m = max(m, w)
            self.hruler.set_range(l, l+w, p, m)
            l,u,p,m = self.vruler.get_range()
            m = max(m, h)
            self.vruler.set_range(l, l+h, p, m)
        self.sw.connect('size-allocate', size_allocate_cb)
        self.area.show()
        self.hruler.show()
        self.vruler.show()
        self.sw.show()
        self.table.show()
        #self.area.show()

    def area_expose_cb(self, area, event):
        self.style = self.area.get_style()
        self.gc = self.style.fg_gc[gtk.STATE_NORMAL]
        for entry in self.drawObjects:
            
            self.draw_rectangle(entry)
        return True



    def draw_rectangle(self,  dicEntry):
        dicEntry['y2'] = dicEntry['y1'] +15
        width = dicEntry['x2'] - dicEntry['x1']
        height = dicEntry['y1'] - dicEntry['y2']
        self.area.window.draw_rectangle(self.gc, False, dicEntry['x1'] *self.Zoom, dicEntry['y1']*self.Zoom,  width*self.Zoom,  height*self.Zoom )
        #self.area.window.draw_rectangle(self.gc, True, x+10, y+10, 20, 20)
        #self.area.window.draw_rectangle(self.gc, True, x+50, y+10, 20, 20)
        #self.area.window.draw_rectangle(self.gc, True, x+20, y+50, 40, 10)
        self.pangolayout.set_text(dicEntry['eName'])
        self.area.window.draw_layout(self.gc, dicEntry['x1']*self.Zoom, dicEntry['y2']*self.Zoom,  self.pangolayout)
        return

    def draw_point(self, x, y):
        self.area.window.draw_point(self.gc, x+30, y+30)
        self.pangolayout.set_text("Point")
        self.area.window.draw_layout(self.gc, x+5, y+50, self.pangolayout)
        return

    def draw_points(self, x, y):
        points = [(x+10,y+10), (x+10,y), (x+40,y+30),
                  (x+30,y+10), (x+50,y+10)]
        self.area.window.draw_points(self.gc, points)
        self.pangolayout.set_text("Points")
        self.area.window.draw_layout(self.gc, x+5, y+50, self.pangolayout)
        return

    def draw_line(self, x, y):
        self.area.window.draw_line(self.gc, x+10, y+10, x+20, y+30)
        self.pangolayout.set_text("Line")
        self.area.window.draw_layout(self.gc, x+5, y+50, self.pangolayout)
        return

    def draw_lines(self, x, y):
        points = [(x+10,y+10), (x+10,y), (x+40,y+30),
                  (x+30,y+10), (x+50,y+10)]
        self.area.window.draw_lines(self.gc, points)
        self.pangolayout.set_text("Lines")
        self.area.window.draw_layout(self.gc, x+5, y+50, self.pangolayout)
        return

    def draw_segments(self, x, y):
        segments = ((x+20,y+10, x+20,y+70), (x+60,y+10, x+60,y+70),
            (x+10,y+30 , x+70,y+30), (x+10, y+50 , x+70, y+50))
        self.area.window.draw_segments(self.gc, segments)
        self.pangolayout.set_text("Segments")
        self.area.window.draw_layout(self.gc, x+5, y+80, self.pangolayout)
        return

    def draw_arcs(self, x, y):
        self.area.window.draw_arc(self.gc, False, x+10, y, 70, 70,
                                  0, 360*64)
        self.area.window.draw_arc(self.gc, True, x+30, y+20, 10, 10,
                                  0, 360*64)
        self.area.window.draw_arc(self.gc, True, x+50, y+20, 10, 10,
                                  0, 360*64)
        self.area.window.draw_arc(self.gc, True, x+30, y+10, 30, 50,
                                  210*64, 120*64)
        self.pangolayout.set_text("Arcs")
        self.area.window.draw_layout(self.gc, x+5, y+80, self.pangolayout)
        return

    def draw_pixmap(self, x, y):
        pixmap, mask = gtk.gdk.pixmap_create_from_xpm(
            self.area.window, self.style.bg[gtk.STATE_NORMAL], "gtk.xpm")

        self.area.window.draw_drawable(self.gc, pixmap, 0, 0, x+15, y+25,
                                       -1, -1)
        self.pangolayout.set_text("Pixmap")
        self.area.window.draw_layout(self.gc, x+5, y+80, self.pangolayout)
        return

    def draw_polygon(self, x, y):
        points = [(x+10,y+60), (x+10,y+20), (x+40,y+70),
                  (x+30,y+30), (x+50,y+40)]
        self.area.window.draw_polygon(self.gc, True, points)
        self.pangolayout.set_text("Polygon")
        self.area.window.draw_layout(self.gc, x+5, y+80, self.pangolayout)
        return

    def draw_rgb_image(self, x, y):
        b = 80*3*80*['\0']
        for i in range(80):
            for j in range(80):
                b[3*80*i+3*j] = chr(255-3*i)
                b[3*80*i+3*j+1] = chr(255-3*abs(i-j))
                b[3*80*i+3*j+2] = chr(255-3*j)
        buff = string.join(b, '')
        self.area.window.draw_rgb_image(self.gc, x, y, 80, 80,
                                 gtk.gdk.RGB_DITHER_NONE, buff, 80*3)
        self.pangolayout.set_text("RGB Image")
        self.area.window.draw_layout(self.gc, x+5, y+80, self.pangolayout)
        return
