;; TODO remove & fix push/pop etc

(defun member (item lst)
  (when lst
    (dolist (i lst)
      (when (= i item)
        (return true)))))

(defun pop (place)
  (return (.pop place)))

(defun push (item place)
  (.push place item))

(defun pushnew (item place)
  (unless (member item place)
    (push item place))
  (return place))

(defun object2alist (obj)
  (when (and obj
             (= "object" (typeof obj))
             (not (length obj)))
    (let ((result (list)))
      (doeach (i obj)
              (push (cons i (slot-value obj i)) result))
      (return result)))) ;; note push adds on the tail!

(defun copy-seq (seq)
  (when seq
    (let ((result (list)))
      (dolist (i seq)
        (push i result)) ;; careful, push puts it at the end! (should be reverse)
      (return result))))

(defun nreverse (seq)
  (when seq
    (return (.reverse seq))))

(defun reverse (seq)
  (return (nreverse (copy-seq seq))))

;;(let ((lst (list 1 2 3 4))) (alert (+ lst #\newline (copy-seq lst))))
;;(let ((lst (list 1 2 3 4))) (alert (+ lst #\newline (reverse lst))))
;;(let ((lst (list 1 2 3 4))) (alert (+ lst #\newline (nreverse lst))))

(defun sort (sequence predicate)
  ;; < relationship
  (.sort sequence
         (lambda (x y)
           (return (if (predicate x y) -1 1))))
  (return sequence))

;;;

(defvar ns (create "xul" "http://www.mozilla.org/keymaster/gatekeeper/there.is.only.xul"
                   "html" "http://www.w3.org/1999/xhtml"))

(defun wget (id doc)
  (return (if doc
              (doc.get-element-by-id id) ;; why this doesn't work (on glade)?
              (document.get-element-by-id id))))

(defvar *whandler* (create))

(defun whandler (sig)
  (when sig
    (let ((h (aref *whandler* sig)))
      (if h
          (return h)
          (return (lambda (e)
                    (alert (+ "Unhandled event " sig "."))))))))

(defun wgetp (w prop)
  ;;(return (w.get-attribute prop)))
  (return (slot-value w prop)))

(defun wsetp (w prop value)
  (w.set-attribute prop value)
  ;;(setf (slot-value w prop) value)
  (return value))

(defun wgets (w style)
  (return (slot-value w.style style)))

(defun wsets (w style value)
  (setf (slot-value w.style style) value)
  ;;tempEl.style.setAttribute('cssText', 'left:150px; top:150px;', 0)
  ;;(w.set-style style value)
  (return value))

(defun wsete (w event handler use-capture)
  (w.add-event-listener event handler (if use-capture true false)))

(defun wunsete (w event handler use-capture)
  (w.remove-event-listener event handler (if use-capture true false)))

(defun wmake (pw tag props sigs)
  (if (= tag "string")
      ;; text
      (let ((w (document.create-text-node props)))
        (when pw
          (pw.append-child w))
        (return w))
      ;; xul or html
      (let ((w (if (tag.match "^xul:")
                   (document.create-element-n-s ns.xul (tag.substring 4))
                   (document.create-element-n-s ns.html tag))))
        (when pw
          (pw.append-child w))
        (when props
          (doeach (i props)
                  (unless (= undefined (slot-value props i))
                    ;;(w.set-attribute i (slot-value props i))
                    (wsetp w i (slot-value props i)))))
        (when sigs
          (doeach (i sigs)
                  (unless (= undefined (slot-value sigs i))
                    #+nil(w.add-event-listener i (whandler (slot-value sigs i)) false)
                    (wsete w i (whandler (slot-value sigs i))))))
        ;;(pw.append-child w)
        (return w))))

(defun wadda (w child)
  (.insert-before (.first-child w) child)
  (return child))

(defun waddz (w child)
  (.append-child w child)
  (return child))

;; function insertAfter(newElement, targetElement)
;; {
;; 	var parent = targetElement.parentNode;
;; 	if(parent.lastChild == targetElement)
;; 	{
;; 		parent.appendChild(newElement);
;; 	}
;; 	else
;; 	{
;; 		parent.insertBefore(newElement, targetElement.nextSibling);
;; 	}
;; }

;; (defun winsert (w pid)
;;   (.insert-before (wget pid) id))

(defun wreplace (w ow nw)
  (.replace-child w nw ow)
  (return nw))

(defun wshow (w)
  (wsets w "visibility" "visible")
  (wsets w "display" ""))

(defun whide (w)
  (wsets w "visibility" "hidden")
  (wsets w "display" "none"))

(defun change-visibility (w show)
  (if show
      (wshow w)
      (whide w)))

(defun toggle-visibility (w)
  (if (= "hidden" (wgets w "visibility"))
      (wshow w)
      (whide w)))

;; widget constructors

(defun wempty (w)
  (when (w.has-child-nodes)
    (dolist (child w.child-nodes)
      (w.remove-child child))))

(defun wremove (w)
  (w.parent-node.remove-child w))

(defun xml-to-string (doc)
  (let ((s (new (*x-m-l-serializer))))
    (return (s.serialize-to-string doc))))

(defun load-xml (url callback)
  ;; http://dean.edwards.name/weblog/2006/04/easy-xml/
  ;; http://www.w3schools.com/xml/xml_parser.asp
  (if window.*active-x-object
      (let ((doc (new (*active-x-object "Microsoft.XMLDOM"))))
        (setf doc.async false)
        (doc.load url)
        (callback doc))
      #+nil(let ((xml (wmake "xml")))
             (setf xml.src url)
             (waddz (wget "body") xml)
             (let ((doc xml.*x-m-l-document))
               (document.body.remove-child xml)
               (callback doc)))
      (if (and document.implementation
               document.implementation.create-document)
          (let ((doc (document.implementation.create-document "" "" nil)))
            (setf doc.onload (lambda () (callback doc)))
            (doc.load url))
          (alert "Your browser cannot handle this script."))))

(defvar *wbuild* (create))

(defvar *wpack* (create))

(defun wclass (widget)
  (if (= widget.class "Custom")
      (return (get-property widget "creation_function"))
      (return widget.class)))

(defun parse-glade (glade)
  ;;(netscape.security.*privilege-manager.enable-privilege "UniversalXPConnect")
  (let ((widgets (create)))
    (labels ((attrs (node)
               (let ((name (node.get-attribute "name"))
                     (value (when node.child-nodes[0]
                              node.child-nodes[0].node-value))
                     (result (create :name name)))
                 (when value
                   (setf result.value value))
                 (dolist (a node.attributes)
                   (setf (slot-value result a.node-name) a.node-value))
                 (return result)))
             (rec-widget (parent node)
               (let ((id (node.get-attribute "id"))
                     (class (node.get-attribute "class"))
                     (widget (create :id id
                                     :parent parent
                                     :children (list)
                                     :class class
                                     :property (create)
                                     :signal (create)
                                     :packing (create))))
                 (when parent
                   (pushnew widget parent.children)) ;; appends!
                 (setf (slot-value widgets id) widget)
                 (rec widget node.child-nodes)
                 ;; TODO return local to widget!
                 (return widget)))
             (rec-child (parent node)
               (let ((current nil))
                 (dolist (child node.child-nodes)
                   (case child.tag-name
                     ("widget" (setf current (rec-widget parent child)))
                     ("packing" (rec-packing parent child current))))))
             (rec-property (parent node)
               (let ((as (attrs node)))
                 (setf (slot-value parent.property as.name) as)))
             (rec-signal (parent node)
               (let ((as (attrs node)))
                 (setf (slot-value parent.signal as.name) as)))
             (rec-packing (parent node current)
               (dolist (child node.child-nodes)
                 (when (= "property" child.tag-name)
                   (let ((as (attrs child)))
                     (setf (slot-value current.packing as.name) as)))))
             (rec (parent nodes current)
               (dolist (node nodes)
                 (case node.tag-name
                   ("glade-interface" (rec parent node.child-nodes))
                   ("widget" (rec-widget parent node))
                   ("child" (rec-child parent node))
                   ("property" (rec-property parent node))
                   ("signal" (rec-signal parent node))
                   ("packing" (rec-packing parent node current))))))
      (rec nil (list glade.document-element)))
    (return widgets)))

(defun wbuild (pw widgets)
  (let ((result nil))
    (dolist (widget widgets)
      (let ((fbuild (aref *wbuild* (wclass widget)))
            (fpack (when (and widget widget.parent)
                     (aref *wpack* (wclass widget.parent))))
            (w (if fbuild
                   (fbuild pw widget)
                   (wmake pw "string" (+ "{ " (wclass widget) " not implemented! }")))))
        (when fpack
          (fpack pw w widget))
        (setf result w)))
    (return result))) ;; return only one for whole container???

(defun get-property (widget name)
  (awhen (slot-value widget.property name)
    (return (slot-value it 'value))))

(defun get-signal (widget name)
  (awhen (slot-value widget.signal name)
    (return (slot-value it 'handler))))

(defun get-packing (widget name)
  (awhen (slot-value widget.packing name)
    (return (slot-value it 'value))))

(defbuild "GtkWindow" ()
  (with-properties (title)
    (if (= "window" pw.tag-name)
        (progn
          (wsetp pw "id" self.id)
          (wsetp pw "title" title)
          (wbuild pw self.children)
          (return pw)) ;; ???
        (let ((w (wmake pw "xul:window" (create :id self.id :title title))))
          (wbuild w self.children)
          (return w)))))

;; <property name="decorated">True</property>
;; <property name="gravity">GDK_GRAVITY_NORTH_WEST</property>

(defpack "GtkWindow" ()
  (let ((resizable (= "True" (get-property self.parent "resizable"))))
    (when resizable
      (wsetp w "flex" 1))))

(defbuild "GtkDialog" ()
  (return (funcall (aref *wbuild* "GtkWindow") pw self)))

(defpack "GtkDialog" ()
  (return (funcall (aref *wpack* "GtkWindow") pw w self)))

(defbuild "GtkButton" ()
  (with-properties (tooltip label sensitive)
    (with-signals (clicked)
      (let ((w (wmake pw "xul:button"
                      (create :id self.id
                              ;;:class-name (get-property self "class-name")
                              :tooltip tooltip
                              :disabled (= "False" sensitive)
                              :label label)
                      (create :command clicked))))
        (wbuild w self.children)
        (return w)))))

(defbuild "GtkCheckButton" ()
  (with-properties (active label)
    (with-signals (toggled)
      (return (wmake pw "xul:checkbox"
                     (create :id self.id
                             :checked (when active true)
                             :label label)
                     (create :command toggled))))))

(defbuild "GtkLabel" ()
  (with-properties (label)
    (return (wmake pw "xul:label" (create :id self.id :value label)))))

(defbuild "GtkEntry" ()
  (with-properties (text tooltip editable)
    (with-signals (changed)
      (return (wmake pw "xul:textbox"
                     (create :id self.id
                             :value text
                             :tooltip tooltip
                             ;; ff3 cant be just (= "False" editable)
                             :readonly (if (= "False" editable)
                                           true
                                           undefined))
                     (create :change changed))))))

(defbuild "GtkTextView" ()
  (with-properties (text tooltip editable)
    (with-signals (changed)
      (return (wmake pw "xul:textbox"
                     (create :id self.id
                             :value text
                             :tooltip tooltip
                             ;; ff3 cant be just (= "False" editable)
                             :readonly (if (= "False" editable)
                                           true
                                           undefined)
                             :multiline t)
                     (create :change changed))))))

(defbuild "GtkFrame" ()
  (let ((w (wmake pw "xul:groupbox" (create :id self.id)))
        (w2 (wmake w "xul:caption"))
        (label (list))
        (body (list)))
    (dolist (child self.children)
      ;; TODO fix label_item... (alert (+ (object2alist child) #\newline "---" #\newline child.packing.type))
      (if (= "label_item" (get-packing child "type"))
          (push child label)
          (push child body)))
    (wbuild w2 label)
    (wbuild w body)))

;; TODO do something meaningful
(defbuild "GtkAlignment" ()
  (wbuild pw self.children)
  #+nil(return ???))

(defbuild "GtkComboBox" ()
  ;; why must be created first and then inserted?
  (with-properties (items)
    (with-signals (changed)
      (let ((w (wmake nil "xul:menulist"
                      (create :id self.id)
                      (create :command changed)))
            (w2 (wmake w "xul:menupopup"))
            (n 0))
        ;;(alert (get-property self "active"))
        (when items
          (dolist (item (.split items #\newline))
            (let ((pair (.split item "|")))
              (wmake w2 "xul:menuitem"
                     (create :value (aref pair 0)
                             :label (or (aref pair 1) (aref pair 0))
                             ;; TODO :selected (when (= n (get-property self "active")) t)
                             )))
            (incf n)))
        (waddz pw w)
        (return w)))))

(defbuild "GtkMenuBar" ()
  (let ((w (wmake nil "xul:menubar" (create :id self.id))))
    (wbuild w self.children)
    (waddz pw w)
    (return w)))

(defbuild "GtkMenu" ()
  (let ((w (wmake pw "xul:menupopup" (create :id self.id))))
    (wbuild w self.children)
    (return w)))

(defbuild "GtkSeparatorMenuItem" ()
  (return (wmake pw "xul:menuseparator" (create :id self.id))))

(defun find-access-key (str)
  ;; use (position item seq)?
  (let ((pos (str.index-of #\_)))
    (unless (minusp pos)
      ;; use (subseq str (1+ pos) (+ 2 pos)))))?
      (return (aref str (1+ pos))))))

;;(alert (find-access-key "hell_o"))
;;(alert (find-access-key "hi"))

(defun remove-access-key (str)
  (return (str.replace #\_ "")))

(defbuild "GtkMenuItem" ()
  ;; used to be (= "menubar" pw.tag-name)
  (with-properties (label)
    (with-signals (activate)
      (if (or (= "GtkMenuBar" (wclass self.parent))
              (plusp (length self.children)))
          (let ((w (wmake pw "xul:menu"
                          (create :id self.id
                                  :label (remove-access-key label)
                                  ;; TODO :acceltext (find-access-key label)
                                  :accesskey (find-access-key label))
                          (create :command activate))))
            (if (plusp (length self.children))
                (wbuild w self.children)
                (wmake w "xul:menupopup"))
            (return w))
          (return (wmake pw "xul:menuitem"
                         (create :id self.id
                                 :label (remove-access-key label)
                                 ;; TODO :acceltext (find-access-key label)
                                 :accesskey (find-access-key label))
                         (create :command activate)))))))

(defbuild "GtkHBox" ()
  (let ((w (wmake pw "xul:hbox"
                  (create :id self.id
                          ;; TODO align for label & combo
                          ;;:equalsize (when (= "True" (get-property self "homogeneous")) "always")
                          ;;:pack "center"
                          :align "center"))))
    (wbuild w self.children)
    (return w)))

(defpack "GtkHBox" ()
  (with-packing (padding expand fill pack_type)
    (when (= "True" expand)
      (wsetp w "flex" 1))
    ;;(wsetp w "pack" "end")
    #+nil(when (= "GTK_PACK_END" pack_type)
           (wsetp w "pack" "end"))))

(defbuild "GtkVBox" ()
  (let ((w (wmake pw "xul:vbox" (create :id self.id))))
    (wbuild w self.children)
    (return w)))

(defpack "GtkVBox" ()
  (with-packing (padding expand fill pack_type)
    (when (= "True" expand)
      (wsetp w "flex" 1))
    ;;(wsetp w "pack" "end")
    #+nil(when (= "GTK_PACK_END" pack_type)
           (wsetp w "pack" "end"))))

(defbuild "GtkHButtonBox" ()
  (let ((w (wmake pw "xul:hbox" (create :id self.id))))
    (wbuild w self.children)
    (return w)))

(defbuild "GtkVButtonBox" ()
  (let ((w (wmake pw "xul:vbox" (create :id self.id))))
    (wbuild w self.children)
    (return w)))

(defbuild "GtkHSeparator" ()
  (return (wmake pw "xul:separator"
                 (create :id self.id
                         :orient "horizontal"
                         :class "groove"))))

(defbuild "GtkVSeparator" ()
  (return (wmake pw "xul:separator"
                 (create :id self.id
                         :orient "vertical"
                         :class "groove"))))

(defbuild "GtkHPaned" ()
  (let ((w (wmake pw "xul:hbox" (create :id self.id)))
        (left self.children[0])
        (right self.children[1]))
    (wbuild w (list left))
    ;; splitters are poor in xul, we do not worry about collapse & resize
    (let ((w2 (wmake w "xul:splitter" (create :id (+ self.id "-splitter")))))
      (wmake w2 "xul:grippy" (create :id (+ self.id "-grippy"))))
    (wbuild w (list right))
    (return w)))

(defpack "GtkHPaned" ()
  (with-packing (shrink resize)
    ;; is this the right test?
    (when (= "True" resize)
      (wsetp w "flex" 1))))

(defbuild "GtkVPaned" ()
  (let ((w (wmake pw "xul:vbox" (create :id self.id)))
        (top self.children[0])
        (bottom self.children[1]))
    (wbuild w (list top))
    (let ((w2 (wmake w "xul:splitter" (create :resizeafter "grow"))))
      (wmake w2 "xul:grippy"))
    (wbuild w (list bottom))
    (return w)))

(defpack "GtkVPaned" ()
  (with-packing (shrink resize)
    ;; TODO
    #+nil(when (= "True" resize)
           (wsetp w "flex" 1))))

(defbuild "GtkNotebook" ()
  (let ((tabs (list))
        (bodies (list)))
    (dolist (child self.children)
      (if (== "tab" (get-packing child "type"))
          (push child tabs) ;; appends!
          (push child bodies)))
    (let ((w (wmake nil "xul:tabbox" (create :id self.id)))
          (w2 (wmake w "xul:tabs"))
          (w3 (wmake w "xul:tabpanels" (create :flex 1))))
      (dolist (tab tabs)
        (let ((w4 (wmake w2 "xul:tab")))
          ;; TODO image?
          (if (= "GtkLabel" tab.class)
              (wsetp w4 "label" tab.property.label.value)
              (wbuild w4 (list tab)))))
      (dolist (body bodies)
        (let ((w5 (wmake w3 "xul:tabpanel")))
          (wbuild w5 (list body))))
      (waddz pw w)
      (return w))))

(defpack "GtkNotebook" ()
  (with-packing (type)
    (let ((expand (= "True" (get-packing self "tab_expand")))
          (fill (= "True" (get-packing self "tab_fill"))))
      (unless (= "tab" type)
        (wsetp w "flex" 1)))))

(defbuild "GtkToolbar" ()
  (let ((w (wmake pw "xul:toolbar"
                  (create :id self.id
                          :align "center")))) ;; like hbox
    (wbuild w self.children)
    (return w)))

(defpack "GtkToolbar" ()
  (with-packing (expand homogeneous)
    ;; TODO homogeneous
    (when (= "True" expand)
      (wsetp w "flex" 1))))

(defbuild "GtkToolItem" ()
  (let ((w (wmake pw "xul:toolbaritem" (create :id self.id))))
    (wbuild w self.children)
    (return w)))

(defbuild "GtkSeparatorToolItem" ()
  ;; why not draw line?
  (let ((w (wmake pw "xul:toolbarseparator" (create :id self.id))))
    ;; TODO why need children?
    (wbuild w self.children)
    (return w)))

(defun image-url (url)
  (when url
    ;; TODO and more like http etc?
    (return (+ "images/" url))))

(defbuild "GtkToolButton" ()
  ;; TODO show label/image
  (with-properties (label icon tooltip)
    (with-signals (clicked)
      (let ((show-label t)
            (show-image t))
        (return (wmake pw "xul:toolbarbutton"
                       (create :id self.id
                               :label (when show-label label)
                               :image (when show-image (image-url icon))
                               :tooltiptext tooltip)
                       (create :command clicked)))))))

(defbuild "GtkImage" ()
  (with-properties (pixbuf)
    (return (wmake pw "xul:image"
                   (create :id self.id :src (image-url pixbuf))))))

(defbuild "GtkProgressBar" ()
  (return (wmake pw "xul:progressmeter"
                 (create :id self.id :mode "determined"))))

(defbuild "GtkStatusbar" ()
  (return (wmake pw "xul:statusbarpanel" (create :id self.id :flex 1)))
  ;; TODO need packhook to set flex of the panel
  #+nil(let ((w (wmake pw "xul:statusbar" (create :id self.id))))
    (wmake w "xul:statusbarpanel" (create :flex 1))
    (return w)))

(defun scan (regexp string)
  (when string
    (return (.match string regexp))))

;;(alert (scan "expand" "asfdexpandasfd"))

;; TODO empty table???
(defbuild "GtkTable" ()
  (let ((n-rows (get-property self "n_rows"))
        (n-columns (get-property self "n_columns"))
        (row-spacing (get-property self "row_spacing"))
        (column-spacing (get-property self "column_spacing"))
        (homogeneous (= "True" (get-property self "homogeneous"))))
    (flet ((earlier (x y)
             (let ((xleft (get-packing x "left_attach"))
                   (xright (get-packing x "right_attach"))
                   (xtop (get-packing x "top_attach"))
                   (xbottom (get-packing x "bottom_attach"))
                   (yleft (get-packing y "left_attach"))
                   (yright (get-packing y "right_attach"))
                   (ytop (get-packing y "top_attach"))
                   (ybottom (get-packing y "bottom_attach"))
                   ;;(c1 (< xtop ytop))
                   ;;(c2 (and (= xtop ytop)
                   ;;(< xleft yleft)))
                   #+nil(c (or c1 c2)))
               #+nil(return (if c -1 1))
               (return (or (< xtop ytop)
                           (and (= xtop ytop)
                                (< xleft yleft))))))
           (getfcols (sorted)
             (unless homogeneous
               (let ((fcols (list))
                     (sorted (copy-seq sorted))
                     (child (pop sorted)))
                 (dotimes (row n-rows)
                   (dotimes (col n-columns)
                     (let ((left (get-packing child "left_attach"))
                           (right (get-packing child "right_attach"))
                           (top (get-packing child "top_attach"))
                           (bottom (get-packing child "bottom_attach"))
                           (x-options (get-packing child "x_options")))
                       (when (and (= top row) (= left col))
                         ;; missing x_options = expand|fill
                         (when (or (null child.packing.x_options)
                                   (scan "expand" x-options))
                           (dotimes (i (1+ (- right left))) ;; 1+?
                             (pushnew col fcols)) ;; appends!
                           #+nil(loop for c from left to right
                                   do (pushnew col fcols)))
                         (setf child (pop sorted))))))
                 (return fcols)))))
      (let ((n-rows (get-property self "n_rows"))
            (n-columns (get-property self "n_columns"))
            (row-spacing (get-property self "row_spacing"))
            (column-spacing (get-property self "column_spacing"))
            (homogeneous (= "True" (get-property self "homogeneous")))
            (sorted (reverse (sort (copy-seq self.children) earlier))) ;; pop works reverse
            (fcols (getfcols sorted))
            (w (wmake pw "xul:grid" (create :id self.id)))
            (w2 (wmake w "xul:columns"))
            (w3 (wmake w "xul:rows")))
        (dotimes (col n-columns)
          ;; TODO homogeneous
          (wmake w2 "xul:column"
                 (create :flex (when (or homogeneous
                                         (member col fcols))
                                 1))))
        (let ((child (pop sorted)))
          (dotimes (row n-rows)
            ;; TODO homogeneous/height
            (let ((w4 (wmake w3 "xul:row" (create :align "center"))))
              (dotimes (col n-columns)
                (let ((left (get-packing child "left_attach"))
                      (right (get-packing child "right_attach"))
                      (top (get-packing child "top_attach"))
                      (bottom (get-packing child "bottom_attach")))
                  (when (and (= top row) (= left col))
                    (wbuild w4 (list child))
                    (setf child (pop sorted))))))))
        (return w)))))

(defbuild "GtkScrolledWindow" ()
  ;; have one child only; packing applies to the child
  (let ((child self.children[0])
        (w (wbuild pw (list child))))
    ;; TODO
    ;;(wsets w "overflow" "auto")
    (return w)))

(defbuild "GtkTreeView" ()
  (return (wmake pw "xul:tree" (create :id self.id)))
  #+nil(labels ((draw-rows (rows)
             (html (:treechildren
                    (dolist (row rows)
                      (let ((cells (cells row))
                            (children (children row)))
                        (html ((:treeitem
                                :when (:container self.children :true)
                                ;;:when (:open self.children :true)
                                )
                               (:treerow (dolist (cell cells)
                                           (html ((:treecell :label cell)))))
                               (when self.children
                                 (draw-rows self.children))))))))))
    (with-properties (model) self
      ;;(format t "~s~%" model)
      (let ((flex (eq (type-of (parent self)) 'GtkScrolledWindow))
            (cols (columns model))
            (scrollbar (eq (type-of (parent self)) 'GtkScrolledWindow))
            (hide-header-row (hide-header-row model)))
        (html ((:tree :id (wid self) :class "GtkTreeView"
                      ;;:when (:style scrollbar "overflow:auto")
                      :when (:hidecolumnpicker (or hide-header-row
                                                   (< (length cols) 2)) :true)
                      :when (:flex flex 1)
                      ;;:enableColumnDrag :true
                      ;;:seltype :single :multiple
                      ;;:disabled :true
                      ;;:when (:align scrollbar :stretch)
                      )
               (when model
                 (html
                  (:treecols
                   (loop for col in cols
                         for n from 0
                         do (destructuring-bind
                                  (cname ctitle cflex chidden cprimary)
                                col
                              (html
                               ((:treecol
                                 :id cname
                                 :when (:primary cprimary :true)
                                 :when (:hideheader hide-header-row :true)
                                 ;;:ignoreincolumnpicker :true
                                 :when (:label (and (not hide-header-row)
                                                    ctitle)
                                               ctitle)
                                 :when (:flex cflex cflex)
                                 :when (:hidden chidden :true))))))))
                 (draw-rows (children model)))))))))

(defbuild "xul:iframe" ()
  (with-properties (string1 string2)
    (return (wmake pw "xul:iframe"
                   (create :id self.id :src string1)
                   (create :load string2)))))

(defun close-window ()
  ;; http://www.interwebby.com/blog/2006/02/04/3/
  (window.open "javascript:window.close();" "_self" ""))

(defun gtk-main-quit ()
  (close-window))
