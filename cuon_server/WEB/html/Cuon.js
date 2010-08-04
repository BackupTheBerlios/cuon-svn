var dicUser = new Array() ;

function main() {
  loadXml
  ('Glade/web_cuon.glade',
   function (glade) {
     var widgets = parseGlade(glade);
     wbuild(document.documentElement, [ widgets['window1'] ]);
   });
};


WHANDLER['on_login1_activate'] =
function (e) {
    var win_login = window.open('',width=50,height=40) ;
    
    
    with (win_login.document){
        loadXml  ('Glade/web_login.glade',   function (glade) {
   
            var widgets = parseGlade(glade);
            wbuild(win_login.document.documentElement, [ widgets['UserID_Dialog'] ]);
            
        }  );
        
        
        WHANDLER['on_okbutton1_clicked'] =
            function () {
                
           
            var userID = win_login.document.getElementById('TUserID').value ;  
            var password = win_login.document.getElementById('TPassword').value ; 
 /*           var rpc = new XmlRpcRequest("http://cuonsim1.de:7086/RPC/","Database.is_running");*/
            var rpc = new XmlRpcRequest("http://cuonsim1.de:7086/RPC/","Database.createSessionID");
             rpc.addParam(userID);
             rpc.addParam(password);   
               var response = rpc.send();
               /*alert(response);
               alert(response.parseXML()); */
                
                
                var sid = response.parseXML();
                dicUser["Name"] = userID ;
                dicUser["SessionID"] = sid ;
                
                win_login.close();
                
                /*chooseClient();*/
            
       };
   };
   };

WHANDLER['delete_event'] =
function () {
    alert('delete_event');
};

WHANDLER['destroy'] =
function () {
    alert('destroy');
    gtkMainQuit();
};
