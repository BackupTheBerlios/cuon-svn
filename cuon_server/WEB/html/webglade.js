function member(item, lst) {
  if (lst) {
    var tmpArr1 = lst;
    if (tmpArr1) {
      for (var tmpI2 = 0; tmpI2 < tmpArr1.length; tmpI2 = tmpI2 + 1) {
        var i = tmpArr1[tmpI2];
        if (i == item) {
          return true;
        };
      };
    };
  };
};

function pop(place) {
  return place.pop();
};

function push(item, place) {
  place.push(item);
};

function pushnew(item, place) {
  if (!member(item, place)) {
    push(item, place);
  };
  return place;
};

function object2alist(obj) {
  if (obj && 'object' == typeof obj && !obj.length) {
    var result = [  ];
    for (var i in obj) {
      push(cons(i, obj[i]), result);
    };
    return result;
  };
};

function copySeq(seq) {
  if (seq) {
    var result = [  ];
    {
      var tmpArr3 = seq;
      if (tmpArr3) {
        for (var tmpI4 = 0; tmpI4 < tmpArr3.length; tmpI4 = tmpI4 + 1) {
          var i = tmpArr3[tmpI4];
          push(i, result);
        };
      };
    };
    return result;
  };
};

function nreverse(seq) {
  if (seq) {
    return seq.reverse();
  };
};

function reverse(seq) {
  return nreverse(copySeq(seq));
};

function sort(sequence, predicate) {
  sequence.sort(function (x, y) {
                  return predicate(x, y) ? -1 : 1;
                });
  return sequence;
};

var ns =
    { 'xul' : 'http://www.mozilla.org/keymaster/gatekeeper/there.is.only.xul', 
      'html' : 'http://www.w3.org/1999/xhtml' };

function wget(id, doc) {
  return doc ? doc.getElementById(id) : document.getElementById(id);
};

var WHANDLER = {  };

function whandler(sig) {
  if (sig) {
    var h = WHANDLER[sig];
    if (h) {
      return h;
    } else {
      return function (e) {
          alert('Unhandled event ' + sig + '.');
        };
    };
  };
};

function wgetp(w, prop) {
  return w[prop];
};

function wsetp(w, prop, value) {
  w.setAttribute(prop, value);
  return value;
};

function wgets(w, style) {
  return w.style[style];
};

function wsets(w, style, value) {
  w.style[style] = value;
  return value;
};

function wsete(w, event, handler, useCapture) {
  w.addEventListener(event, handler, useCapture ? true : false);
};

function wunsete(w, event, handler, useCapture) {
  w.removeEventListener(event, handler, useCapture ? true : false);
};

function wmake(pw, tag, props, sigs) {
  if (tag == 'string') {
    var w = document.createTextNode(props);
    if (pw) {
      pw.appendChild(w);
    };
    return w;
  } else {
    var w =
        tag.match('^xul:') ?
          document.createElementNS(ns.xul, tag.substring(4)) :
          document.createElementNS(ns.html, tag);
    if (pw) {
      pw.appendChild(w);
    };
    if (props) {
      for (var i in props) {
        if (undefined != props[i]) {
          wsetp(w, i, props[i]);
        };
      };
    };
    if (sigs) {
      for (var i in sigs) {
        if (undefined != sigs[i]) {
          wsete(w, i, whandler(sigs[i]));
        };
      };
    };
    return w;
  };
};

function wadda(w, child) {
  w.firstChild().insertBefore(child);
  return child;
};

function waddz(w, child) {
  w.appendChild(child);
  return child;
};

function wreplace(w, ow, nw) {
  w.replaceChild(nw, ow);
  return nw;
};

function wshow(w) {
  wsets(w, 'visibility', 'visible');
  wsets(w, 'display', '');
};

function whide(w) {
  wsets(w, 'visibility', 'hidden');
  wsets(w, 'display', 'none');
};

function changeVisibility(w, show) {
  if (show) {
    wshow(w);
  } else {
    whide(w);
  };
};

function toggleVisibility(w) {
  if ('hidden' == wgets(w, 'visibility')) {
    wshow(w);
  } else {
    whide(w);
  };
};

function wempty(w) {
  if (w.hasChildNodes()) {
    var tmpArr5 = w.childNodes;
    if (tmpArr5) {
      for (var tmpI6 = 0; tmpI6 < tmpArr5.length; tmpI6 = tmpI6 + 1) {
        var child = tmpArr5[tmpI6];
        w.removeChild(child);
      };
    };
  };
};

function wremove(w) {
  w.parentNode.removeChild(w);
};

function xmlToString(doc) {
  var s = new XMLSerializer();
  return s.serializeToString(doc);
};

function loadXml(url, callback) {
  if (window.ActiveXObject) {
    var doc = new ActiveXObject('Microsoft.XMLDOM');
    doc.async = false;
    doc.load(url);
    callback(doc);
  } else {
    if (document.implementation && document.implementation.createDocument) {
      var doc = document.implementation.createDocument('', '', null);
      doc.onload =
      function () {
        callback(doc);
      };
      doc.load(url);
    } else {
      alert('Your browser cannot handle this script.');
    };
  };
};

var WBUILD = {  };

var WPACK = {  };

function wclass(widget) {
  if (widget.class == 'Custom') {
    return getProperty(widget, 'creation_function');
  } else {
    return widget.class;
  };
};

function parseGlade(glade) {
  var widgets = {  };
  {
    var attrs =
        function (node) {
          var name = node.getAttribute('name');
          var value =
              node.childNodes[0] ? node.childNodes[0].nodeValue : undefined;
          var result = { name : name };
          if (value) {
            result.value = value;
          };
          {
            var tmpArr7 = node.attributes;
            if (tmpArr7) {
              for (var tmpI8 = 0; tmpI8 < tmpArr7.length;
                   tmpI8 = tmpI8 + 1) {
                var a = tmpArr7[tmpI8];
                result[a.nodeName] = a.nodeValue;
              };
            };
          };
          return result;
        };
    var recWidget =
        function (parent, node) {
          var id = node.getAttribute('id');
          var class = node.getAttribute('class');
          var widget =
              { id : id, 
                parent : parent, 
                children : [  ], 
                class : class, 
                property : {  }, 
                signal : {  }, 
                packing : {  } };
          if (parent) {
            pushnew(widget, parent.children);
          };
          widgets[id] = widget;
          rec(widget, node.childNodes);
          return widget;
        };
    var recChild =
        function (parent, node) {
          var current = null;
          var tmpArr9 = node.childNodes;
          if (tmpArr9) {
            for (var tmpI10 = 0; tmpI10 < tmpArr9.length;
                 tmpI10 = tmpI10 + 1) {
              var child = tmpArr9[tmpI10];
              switch (child.tagName) {
                case 'widget':
                   current = recWidget(parent, child);
                   break;
                case 'packing':   recPacking(parent, child, current);
              };
            };
          };
        };
    var recProperty =
        function (parent, node) {
          var as = attrs(node);
          parent.property[as.name] = as;
        };
    var recSignal =
        function (parent, node) {
          var as = attrs(node);
          parent.signal[as.name] = as;
        };
    var recPacking =
        function (parent, node, current) {
          var tmpArr11 = node.childNodes;
          if (tmpArr11) {
            for (var tmpI12 = 0; tmpI12 < tmpArr11.length;
                 tmpI12 = tmpI12 + 1) {
              var child = tmpArr11[tmpI12];
              if ('property' == child.tagName) {
                var as = attrs(child);
                current.packing[as.name] = as;
              };
            };
          };
        };
    var rec =
        function (parent, nodes, current) {
          var tmpArr13 = nodes;
          if (tmpArr13) {
            for (var tmpI14 = 0; tmpI14 < tmpArr13.length;
                 tmpI14 = tmpI14 + 1) {
              var node = tmpArr13[tmpI14];
              switch (node.tagName) {
                case 'glade-interface':
                   rec(parent, node.childNodes);
                   break;
                case 'widget':
                   recWidget(parent, node);
                   break;
                case 'child':
                   recChild(parent, node);
                   break;
                case 'property':
                   recProperty(parent, node);
                   break;
                case 'signal':
                   recSignal(parent, node);
                   break;
                case 'packing':   recPacking(parent, node, current);
              };
            };
          };
        };
    rec(null, [ glade.documentElement ]);
  };
  return widgets;
};

function wbuild(pw, widgets) {
  var result = null;
  {
    var tmpArr15 = widgets;
    if (tmpArr15) {
      for (var tmpI16 = 0; tmpI16 < tmpArr15.length; tmpI16 = tmpI16 + 1) {
        var widget = tmpArr15[tmpI16];
        var fbuild = WBUILD[wclass(widget)];
        var fpack =
            widget && widget.parent ? WPACK[wclass(widget.parent)] :
              undefined;
        var w =
            fbuild ? fbuild(pw, widget) :
              wmake
              (pw, 'string', '{ ' + wclass(widget) + ' not implemented! }');
        if (fpack) {
          fpack(pw, w, widget);
        };
        result = w;
      };
    };
  };
  return result;
};

function getProperty(widget, name) {
  var it = widget.property[name];
  if (it) {
    return it.value;
  };
};

function getSignal(widget, name) {
  var it = widget.signal[name];
  if (it) {
    return it.handler;
  };
};

function getPacking(widget, name) {
  var it = widget.packing[name];
  if (it) {
    return it.value;
  };
};

WBUILD['GtkWindow'] =
function (pw, self) {
  var title = getProperty(self, 'title');
  if ('window' == pw.tagName) {
    wsetp(pw, 'id', self.id);
    wsetp(pw, 'title', title);
    wbuild(pw, self.children);
    return pw;
  } else {
    var w =
        wmake
        (pw, 'xul:window',
         { id : self.id, 
           title : title });
    wbuild(w, self.children);
    return w;
  };
};

WPACK['GtkWindow'] =
function (pw, w, self) {
  var resizable = 'True' == getProperty(self.parent, 'resizable');
  if (resizable) {
    wsetp(w, 'flex', 1);
  };
};

WBUILD['GtkDialog'] =
function (pw, self) {
  return WBUILD['GtkWindow'](pw, self);
};

WPACK['GtkDialog'] =
function (pw, w, self) {
  return WPACK['GtkWindow'](pw, w, self);
};

WBUILD['GtkButton'] =
function (pw, self) {
  var tooltip = getProperty(self, 'tooltip');
  var label = getProperty(self, 'label');
  var sensitive = getProperty(self, 'sensitive');
  var clicked = getSignal(self, 'clicked');
  var w =
      wmake
      (pw, 'xul:button',
       { id : self.id, 
         tooltip : tooltip, 
         disabled : 'False' == sensitive, 
         label : label },
       { command : clicked });
  wbuild(w, self.children);
  return w;
};

WBUILD['GtkCheckButton'] =
function (pw, self) {
  var active = getProperty(self, 'active');
  var label = getProperty(self, 'label');
  var toggled = getSignal(self, 'toggled');
  return wmake
    (pw, 'xul:checkbox',
     { id : self.id, 
       checked : active ? true : undefined, 
       label : label },
     { command : toggled });
};

  WBUILD['GtkRadioButton'] =
  function (pw, self) {
    var active = getProperty(self, 'active');
    var label = getProperty(self, 'label');
    var group = getProperty(self, 'group');
    return wmake
      (pw, 'html:input',
       { id : self.id, 
         type : "radio",
         checked : active ? true : undefined, 
         label : label , 
         name : group },
       { });
  };
  
  
WBUILD['GtkLabel'] =
function (pw, self) {
  var label = getProperty(self, 'label');
  return wmake
    (pw, 'xul:label',
     { id : self.id, 
       value : label });
};

WBUILD['GtkEntry'] =
function (pw, self) {
  var text = getProperty(self, 'text');
  var tooltip = getProperty(self, 'tooltip');
  var editable = getProperty(self, 'editable');
  var changed = getSignal(self, 'changed');
  return wmake
    (pw, 'xul:textbox',
     { id : self.id, 
       value : text, 
       tooltip : tooltip, 
       readonly : 'False' == editable ? true : undefined },
     { change : changed });
};

WBUILD['GtkTextView'] =
function (pw, self) {
  var text = getProperty(self, 'text');
  var tooltip = getProperty(self, 'tooltip');
  var editable = getProperty(self, 'editable');
  var changed = getSignal(self, 'changed');
  return wmake
    (pw, 'xul:textbox',
     { id : self.id, 
       value : text, 
       tooltip : tooltip, 
       readonly : 'False' == editable ? true : undefined, 
       multiline : true },
     { change : changed });
};

WBUILD['GtkTreeView'] =
function (pw, self) {
  
  var row_activated = getSignal(self, 'row-activated');
  return wmake
    (pw, 'xul:listbox',
     { id : self.id  }
     );
};

WBUILD['GtkFrame'] =
function (pw, self) {
  var w = wmake(pw, 'xul:groupbox', { id : self.id });
  var w2 = wmake(w, 'xul:caption');
  var label = [  ];
  var body = [  ];
  {
    var tmpArr17 = self.children;
    if (tmpArr17) {
      for (var tmpI18 = 0; tmpI18 < tmpArr17.length; tmpI18 = tmpI18 + 1) {
        var child = tmpArr17[tmpI18];
        if ('label_item' == getPacking(child, 'type')) {
          push(child, label);
        } else {
          push(child, body);
        };
      };
    };
  };
  wbuild(w2, label);
  wbuild(w, body);
};

WBUILD['GtkAlignment'] =
function (pw, self) {
  wbuild(pw, self.children);
};

WBUILD['GtkComboBox'] =
function (pw, self) {
  var items = getProperty(self, 'items');
  var changed = getSignal(self, 'changed');
  var w =
      wmake(null, 'xul:menulist', { id : self.id }, { command : changed });
  var w2 = wmake(w, 'xul:menupopup');
  var n = 0;
  if (items) {
    var tmpArr19 = items.split('\n');
    if (tmpArr19) {
      for (var tmpI20 = 0; tmpI20 < tmpArr19.length;
           tmpI20 = tmpI20 + 1) {
        var item = tmpArr19[tmpI20];
        {
          var pair = item.split('|');
          wmake
          (w2, 'xul:menuitem',
           { value : pair[0], 
             label : pair[1] || pair[0] });
        };
        ++n;
      };
    };
  };
  waddz(pw, w);
  return w;
};

WBUILD['GtkMenuBar'] =
function (pw, self) {
  var w = wmake(null, 'xul:menubar', { id : self.id });
  wbuild(w, self.children);
  waddz(pw, w);
  return w;
};

WBUILD['GtkMenu'] =
function (pw, self) {
  var w = wmake(pw, 'xul:menupopup', { id : self.id });
  wbuild(w, self.children);
  return w;
};

WBUILD['GtkSeparatorMenuItem'] =
function (pw, self) {
  return wmake(pw, 'xul:menuseparator', { id : self.id });
};

function findAccessKey(str) {
  var pos = str.indexOf('_');
  if (pos >= 0) {
    return str[pos + 1];
  };
};

function removeAccessKey(str) {
  return str.replace('_', '');
};

WBUILD['GtkMenuItem'] =
function (pw, self) {
  var label = getProperty(self, 'label');
  var activate = getSignal(self, 'activate');
  if ('GtkMenuBar' == wclass(self.parent) || 0 < self.children.length) {
    var w =
        wmake
        (pw, 'xul:menu',
         { id : self.id, 
           label : removeAccessKey(label), 
           accesskey : findAccessKey(label) },
         { command : activate });
    if (0 < self.children.length) {
      wbuild(w, self.children);
    } else {
      wmake(w, 'xul:menupopup');
    };
    return w;
  } else {
    return wmake
      (pw, 'xul:menuitem',
       { id : self.id, 
         label : removeAccessKey(label), 
         accesskey : findAccessKey(label) },
       { command : activate });
  };
};

WBUILD['GtkImageMenuItem'] =
function (pw, self) {
  var label = getProperty(self, 'label');
  var activate = getSignal(self, 'activate');
  if ('GtkMenuBar' == wclass(self.parent) || 0 < self.children.length) {
    var w =
        wmake
        (pw, 'xul:menu',
         { id : self.id, 
           label : removeAccessKey(label), 
           accesskey : findAccessKey(label) },
         { command : activate });
    if (0 < self.children.length) {
      wbuild(w, self.children);
    } else {
      wmake(w, 'xul:menupopup');
    };
    return w;
  } else {
    return wmake
      (pw, 'xul:menuitem',
       { id : self.id, 
         label : removeAccessKey(label), 
         accesskey : findAccessKey(label) },
       { command : activate });
  };
};

WBUILD['GtkHBox'] =
function (pw, self) {
  var w =
      wmake
      (pw, 'xul:hbox',
       { id : self.id, 
         align : 'center' });
  wbuild(w, self.children);
  return w;
};

WPACK['GtkHBox'] =
function (pw, w, self) {
  var padding = getPacking(self, 'padding');
  var expand = getPacking(self, 'expand');
  var fill = getPacking(self, 'fill');
  var pack_type = getPacking(self, 'pack_type');
  if ('True' == expand) {
    wsetp(w, 'flex', 1);
  };
};

WBUILD['GtkVBox'] =
function (pw, self) {
  var w = wmake(pw, 'xul:vbox', { id : self.id });
  wbuild(w, self.children);
  return w;
};

WPACK['GtkVBox'] =
function (pw, w, self) {
  var padding = getPacking(self, 'padding');
  var expand = getPacking(self, 'expand');
  var fill = getPacking(self, 'fill');
  var pack_type = getPacking(self, 'pack_type');
  if ('True' == expand) {
    wsetp(w, 'flex', 1);
  };
};

WBUILD['GtkHButtonBox'] =
function (pw, self) {
  var w = wmake(pw, 'xul:hbox', { id : self.id });
  wbuild(w, self.children);
  return w;
};

WBUILD['GtkVButtonBox'] =
function (pw, self) {
  var w = wmake(pw, 'xul:vbox', { id : self.id });
  wbuild(w, self.children);
  return w;
};

WBUILD['GtkHSeparator'] =
function (pw, self) {
  return wmake
    (pw, 'xul:separator',
     { id : self.id, 
       orient : 'horizontal', 
       class : 'groove' });
};

WBUILD['GtkVSeparator'] =
function (pw, self) {
  return wmake
    (pw, 'xul:separator',
     { id : self.id, 
       orient : 'vertical', 
       class : 'groove' });
};

WBUILD['GtkHPaned'] =
function (pw, self) {
  var w = wmake(pw, 'xul:hbox', { id : self.id });
  var left = self.children[0];
  var right = self.children[1];
  wbuild(w, [ left ]);
  {
    var w2 = wmake(w, 'xul:splitter', { id : self.id + '-splitter' });
    wmake(w2, 'xul:grippy', { id : self.id + '-grippy' });
  };
  wbuild(w, [ right ]);
  return w;
};

WPACK['GtkHPaned'] =
function (pw, w, self) {
  var shrink = getPacking(self, 'shrink');
  var resize = getPacking(self, 'resize');
  if ('True' == resize) {
    wsetp(w, 'flex', 1);
  };
};

WBUILD['GtkVPaned'] =
function (pw, self) {
  var w = wmake(pw, 'xul:vbox', { id : self.id });
  var top = self.children[0];
  var bottom = self.children[1];
  wbuild(w, [ top ]);
  {
    var w2 = wmake(w, 'xul:splitter', { resizeafter : 'grow' });
    wmake(w2, 'xul:grippy');
  };
  wbuild(w, [ bottom ]);
  return w;
};

WPACK['GtkVPaned'] =
function (pw, w, self) {
  var shrink = getPacking(self, 'shrink');
  var resize = getPacking(self, 'resize');
};

WBUILD['GtkNotebook'] =
function (pw, self) {
  var tabs = [  ];
  var bodies = [  ];
  {
    var tmpArr21 = self.children;
    if (tmpArr21) {
      for (var tmpI22 = 0; tmpI22 < tmpArr21.length; tmpI22 = tmpI22 + 1) {
        var child = tmpArr21[tmpI22];
        if ('tab' == getPacking(child, 'type')) {
          push(child, tabs);
        } else {
          push(child, bodies);
        };
      };
    };
  };
  var w = wmake(null, 'xul:tabbox', { id : self.id });
  var w2 = wmake(w, 'xul:tabs');
  var w3 = wmake(w, 'xul:tabpanels', { flex : 1 });
  {
    var tmpArr23 = tabs;
    if (tmpArr23) {
      for (var tmpI24 = 0; tmpI24 < tmpArr23.length; tmpI24 = tmpI24 + 1) {
        var tab = tmpArr23[tmpI24];
        var w4 = wmake(w2, 'xul:tab');
        if ('GtkLabel' == tab.class) {
          wsetp(w4, 'label', tab.property.label.value);
        } else {
          wbuild(w4, [ tab ]);
        };
      };
    };
  };
  {
    var tmpArr25 = bodies;
    if (tmpArr25) {
      for (var tmpI26 = 0; tmpI26 < tmpArr25.length; tmpI26 = tmpI26 + 1) {
        var body = tmpArr25[tmpI26];
        var w5 = wmake(w3, 'xul:tabpanel');
        wbuild(w5, [ body ]);
      };
    };
  };
  waddz(pw, w);
  return w;
};

WPACK['GtkNotebook'] =
function (pw, w, self) {
  var type = getPacking(self, 'type');
  var expand = 'True' == getPacking(self, 'tab_expand');
  var fill = 'True' == getPacking(self, 'tab_fill');
  if ('tab' != type) {
    wsetp(w, 'flex', 1);
  };
};

WBUILD['GtkToolbar'] =
function (pw, self) {
  var w =
      wmake
      (pw, 'xul:toolbar',
       { id : self.id, 
         align : 'center' });
  wbuild(w, self.children);
  return w;
};

WPACK['GtkToolbar'] =
function (pw, w, self) {
  var expand = getPacking(self, 'expand');
  var homogeneous = getPacking(self, 'homogeneous');
  if ('True' == expand) {
    wsetp(w, 'flex', 1);
  };
};

WBUILD['GtkToolItem'] =
function (pw, self) {
  var w = wmake(pw, 'xul:toolbaritem', { id : self.id });
  wbuild(w, self.children);
  return w;
};

WBUILD['GtkSeparatorToolItem'] =
function (pw, self) {
  var w = wmake(pw, 'xul:toolbarseparator', { id : self.id });
  wbuild(w, self.children);
  return w;
};

function imageUrl(url) {
  if (url) {
    return 'images/' + url;
  };
};

WBUILD['GtkToolButton'] =
function (pw, self) {
  var label = getProperty(self, 'label');
  var icon = getProperty(self, 'icon');
  var tooltip = getProperty(self, 'tooltip');
  var clicked = getSignal(self, 'clicked');
  var showLabel = true;
  var showImage = true;
  return wmake
    (pw, 'xul:toolbarbutton',
     { id : self.id, 
       label : showLabel ? label : undefined, 
       image : showImage ? imageUrl(icon) : undefined, 
       tooltiptext : tooltip },
     { command : clicked });
};

WBUILD['GtkImage'] =
function (pw, self) {
  var pixbuf = getProperty(self, 'pixbuf');
  return wmake
    (pw, 'xul:image',
     { id : self.id, 
       src : imageUrl(pixbuf) });
};

WBUILD['GtkProgressBar'] =
function (pw, self) {
  return wmake
    (pw, 'xul:progressmeter',
     { id : self.id, 
       mode : 'determined' });
};

WBUILD['GtkStatusbar'] =
function (pw, self) {
  return wmake
    (pw, 'xul:statusbarpanel',
     { id : self.id, 
       flex : 1 });
};

function scan(regexp, string) {
  if (string) {
    return string.match(regexp);
  };
};

WBUILD['GtkTable'] =
function (pw, self) {
  var nRows = getProperty(self, 'n_rows');
  var nColumns = getProperty(self, 'n_columns');
  var rowSpacing = getProperty(self, 'row_spacing');
  var columnSpacing = getProperty(self, 'column_spacing');
  var homogeneous = 'True' == getProperty(self, 'homogeneous');
  var earlier =
      function (x, y) {
        var xleft = getPacking(x, 'left_attach');
        var xright = getPacking(x, 'right_attach');
        var xtop = getPacking(x, 'top_attach');
        var xbottom = getPacking(x, 'bottom_attach');
        var yleft = getPacking(y, 'left_attach');
        var yright = getPacking(y, 'right_attach');
        var ytop = getPacking(y, 'top_attach');
        var ybottom = getPacking(y, 'bottom_attach');
        return xtop < ytop || xtop == ytop && xleft < yleft;
      };
  var getfcols =
      function (sorted) {
        if (!homogeneous) {
          var fcols = [  ];
          var sorted = copySeq(sorted);
          var child = pop(sorted);
          for (var row = 0; row < nRows; row = row + 1) {
            for (var col = 0; col < nColumns; col = col + 1) {
              var left = getPacking(child, 'left_attach');
              var right = getPacking(child, 'right_attach');
              var top = getPacking(child, 'top_attach');
              var bottom = getPacking(child, 'bottom_attach');
              var xOptions = getPacking(child, 'x_options');
              if (top == row && left == col) {
                if (null == child.packing.x_options || scan('expand', xOptions)) {
                  for (var i = 0; i < (right - left) + 1;
                       i = i + 1) {
                    pushnew(col, fcols);
                  };
                };
                child = pop(sorted);
              };
            };
          };
          return fcols;
        };
      };
  var nRows = getProperty(self, 'n_rows');
  var nColumns = getProperty(self, 'n_columns');
  var rowSpacing = getProperty(self, 'row_spacing');
  var columnSpacing = getProperty(self, 'column_spacing');
  var homogeneous = 'True' == getProperty(self, 'homogeneous');
  var sorted = reverse(sort(copySeq(self.children), earlier));
  var fcols = getfcols(sorted);
  var w = wmake(pw, 'xul:grid', { id : self.id });
  var w2 = wmake(w, 'xul:columns');
  var w3 = wmake(w, 'xul:rows');
  for (var col = 0; col < nColumns; col = col + 1) {
    wmake
    (w2, 'xul:column',
     { flex : homogeneous || member(col, fcols) ? 1 : undefined });
  };
  {
    var child = pop(sorted);
    for (var row = 0; row < nRows; row = row + 1) {
      var w4 = wmake(w3, 'xul:row', { align : 'center' });
      for (var col = 0; col < nColumns; col = col + 1) {
        var left = getPacking(child, 'left_attach');
        var right = getPacking(child, 'right_attach');
        var top = getPacking(child, 'top_attach');
        var bottom = getPacking(child, 'bottom_attach');
        if (top == row && left == col) {
          wbuild(w4, [ child ]);
          child = pop(sorted);
        };
      };
    };
  };
  return w;
};

WBUILD['GtkScrolledWindow'] =
function (pw, self) {
  var child = self.children[0];
  var w = wbuild(pw, [ child ]);
  return w;
};

WBUILD['GtkTreeView'] =
function (pw, self) {
  return wmake(pw, 'xul:tree', { id : self.id });
};

WBUILD['xul:iframe'] =
function (pw, self) {
  var string1 = getProperty(self, 'string1');
  var string2 = getProperty(self, 'string2');
  return wmake
    (pw, 'xul:iframe',
     { id : self.id, 
       src : string1 },
     { load : string2 });
};

function closeWindow() {
  window.open('javascript:window.close();', '_self', '');
};

function gtkMainQuit() {
  closeWindow();
};

