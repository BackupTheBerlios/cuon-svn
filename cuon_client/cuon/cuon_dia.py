import sys, dia
from xmlrpclib import ServerProxy

class MyXmlrpc:


    	def __init__(self):
        	print 'load Xmlrpc'
        	self.xmlrpcserver = 'http://localhost:7080'
        	self.MyServer = self.getMyServer()


	def getMyServer(self):
	        print 'get Server'
	        sv = None
	        try:
	            sv = ServerProxy(self.xmlrpcserver,allow_none = 1)
	        except Exception,  params:
	            print Exception, params
	        print 'sv = ' ,  sv    
	        return sv

	def test(self):
	        print 'Test xmlrpc1'
	        print self.MyServer
	
	        #if self.MyServer:
	        #    print 'Test xmlrpc2'
	        #    print self.MyServer
	        print self.MyServer.Database.testXmlrpc(7, 5)
		dicAllObjects = {}
		dicAllObjects['o1'] = 'Value1'

		
		print self.MyServer.Misc.saveDia('test', dicAllObjects)
		
	
			
	        return True


class CuonDia :


	def __init__(self, diagram, data, props):
		import pygtk
		pygtk.require("2.0")
		import gtk
		print 'cuon dia'
		props = ['1', '2']
		self.diagram  = dia.active_display().diagram
		self.data = data
		self.props = props

		self.win = gtk.Window ()
		self.win.connect("delete_event", self.on_delete)
		self.win.set_title("Cuon")
        
		box1 = gtk.VBox()
		self.win.add(box1)
		box1.show()
        
		box2 = gtk.VBox(spacing=2)
		box2.set_border_width(10)
		box1.pack_start(box2)
		box2.show()
        
		self.checkboxes = []
		self.optionmenues = []
		table = gtk.Table(2, len(props), 0)
		table.set_row_spacings(2)
		table.set_col_spacings(5)
		table.set_border_width(5)
		y = 0
        
		box2.pack_start(table)
		table.show()
        
		separator = gtk.HSeparator()
		box1.pack_start(separator, expand=0)
		separator.show()
        
		box2 = gtk.VBox(spacing=10)
		box2.set_border_width(10)
		box1.pack_start(box2, expand=0)
		box2.show()
        
		button = gtk.Button("Ok")
		button.connect("clicked", self.on_ok)
		box2.pack_start(button)
		button.set_flags(gtk.CAN_DEFAULT)
		button.grab_default()
		button.show()
		self.win.show()
		self.rpc = MyXmlrpc()
		#print self.rpc.test()
		#self.createCuonObject('Network - A Desktop PC', 20, 20)
		
	def on_ok (self, *args) :
		grp = self.diagram.get_sorted_selected()
		
		
		self.diagram.flush()
		dicAllObjects = {}
		dicAllObjects['o1'] = 'Value1'
		print self.diagram
#		diagramData = self.diagram.data
#		print diagramData
#		dicLayers = diagramData.layers
#		print dicLayers
#		for onelayer in dicLayers:
#			print onelayer
#			print onelayer.name
#			for layerObject in onelayer.objects:
#				print layerObject
#				print layerObject.bounding_box
#				print layerObject.bounding_box.top
#				print layerObject.bounding_box.left
#				print layerObject.bounding_box.right
#				print layerObject.bounding_box.bottom
#
#				print layerObject.connections
#				for oneConnection in layerObject.connections:
#					print oneConnection.pos
#					print oneConnection.connected
#					
#					
#				


				
		self.diagram.save('test999.dia')
		f = open('test999.dia')
		s = f.read()
		
		print self.rpc.MyServer.Misc.saveDia('test5', s)
		f.close()
		
				
		
		self.win.destroy()

	def on_delete (self, *args) :		
		self.win.destroy ()

		
	def createCuonObject(self,st,cx,cy):


		diagram = dia.new("Cuon Objects.dia")
		data = diagram.data
		#layer = data.active_layer
		layer = data.add_layer ('Network')
		print layer
		o, h1, h2 = dia.get_object_type(st).create (cx, cy)
		print 'o = ',  o
		w = o.bounding_box.right - o.bounding_box.left
		h = o.bounding_box.bottom - o.bounding_box.top
		o.move (cx, cy)               
		print 'move',  cx,  cy
		layer.add_object (o)
		layer.update_extents()
		data.update_extents()
		print 'data updated'
		if diagram :
			print 'show diagram'
			diagram.display()
			diagram.flush()
			






class PropInfo :
	def __init__ (self, t, n, o) :
		self.num = 1
		self.type = t
		self.name = n
		self.opts = [o]

	def __str__ (self) :
		return self.name + ":" + str(self.opts)
	def Add (self, o) :
		self.num = self.num + 1
		self.opts.append(o)

def dia_objects_props_cb (data, flags) :

	d = dia.active_display().diagram
	
	# display the dialog
	data = None
	allProps = None
	dlg = CuonDia(d, data, allProps)

dia.register_action ("CuonDia", "Cuon Dia ", 
                      "/DisplayMenu/Dialogs/DialogsExtensionStart", 
                       dia_objects_props_cb)

