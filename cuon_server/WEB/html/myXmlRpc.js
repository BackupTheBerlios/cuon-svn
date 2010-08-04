
/*
 
Simple xmlrpc client for sending requests and receiving results via a callback using standard Titanium http client mechanics.
 
Spec: http://www.xmlrpc.com/spec
 
*/
 
// string url: the full url to the server side xmlrpc script
// string method: the name of the xmlrpc method to call
// array params: list of strings to send
// func callback: callback function to call "onload"
function xmlrpc(url, method, params, callback)
{
    Titanium.API.info("xmlrpc: begin");
    Titanium.API.info("xmlrpc: url: " + url);
    Titanium.API.info("xmlrpc: method: " + method);
 
    var xhr = Titanium.Network.createHTTPClient();
    xhr.open("POST",url);
    xhr.onload = callback;
    var xml = '<methodCall>';
    xml += '<methodName>'+method+'</methodName>';
    xml += '<params>';
    for (var k in params)
    {
        if (k)
        {
            var p = params[k];
            Titanium.API.info("xmlrpc: p: "+p);
            xml += '<param><string>'+p+'</string></param>';
        }
    }
    xml += '</params></methodCall>';
    Titanium.API.info("xmlrpc: xml: "+xml);
    xhr.send(xml);
    Titanium.API.info("xmlrpc: end");
}

