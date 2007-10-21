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
	        return True

class CuonDia :


	def __init__(self, diagram, data, props):
		import pygtk
		pygtk.require("2.0")
		import gtk
		print 'cuon dia'
		self.diagram = diagram
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
		rpc = MyXmlrpc()
		print rpc.test()
		self.createCuonObject('Network - A Desktop PC', 20, 20)
		
	def on_ok (self, *args) :
		grp = self.diagram.get_sorted_selected()
		
		# change the requested properties
		for i in range(0, len(self.checkboxes)) :
			cb = self.checkboxes[i]
			om = self.optionmenues[i]
			if cb.get_active() :
				for o in grp :
					s = self.props.keys()[i]
					o.properties[s] = self.props[s].opts[om.get_history()]
		self.data.update_extents ()
		self.diagram.flush()
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
	grp = d.get_sorted_selected()
	allProps = {}
	numProps = len(grp)


	# check for properties common to all select objects
	for o in grp :
		props = o.properties
		for s in props.keys() :
			if props[s].visible :
				if allProps.has_key(s) :
					allProps[s].Add(props[s])
				else :
					allProps[s] = PropInfo(props[s].type, props[s].name, props[s])
	# now eliminate all props not common ...
	for s in allProps.keys() :
		if allProps[s].num < numProps :
			del allProps[s]
	# ... and all props already equal
	for s in allProps.keys() :
		o1 = allProps[s].opts[0]
		for o in allProps[s].opts :
			if o1.value != o.value :
				o1 = None
				break
		if o1 != None :
			del allProps[s]
		else :
			# if there is something left ensure unique values
			uniques = {}
			for o in allProps[s].opts :
				if uniques.has_key(o.value) :
					continue
				uniques[o.value] = o
			allProps[s].opts = []
			for v in uniques.keys() :
				allProps[s].opts.append(uniques[v])
	# display the dialog
	dlg = CuonDia(d, data, allProps)

dia.register_action ("CuonDia", "Cuon Dia ", 
                      "/DisplayMenu/Dialogs/DialogsExtensionStart", 
                       dia_objects_props_cb)

