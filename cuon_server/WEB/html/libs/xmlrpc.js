/*
 * Copyright (c) 2010 Sven Ludwig
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to
 * deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 *
 */

var XMLRPC = function(url, method, parameters, callback, failCallback) {

  var Prepare = function() {
    return this;
  }

  Prepare.prototype.eval = function(value) {
    if (typeof value == 'object' ) {
      if (value instanceof Object) {
        var nvalue={ struct: { member: new Array() } }
        var pos=0;
        for ( elem in value ) {
          nvalue.struct.member[pos]={name: elem, value: this.eval(value[elem]).value};
          pos++;
        }
      } else {
        var nvalue={ array: { data: new Array() } }
        for (var j=0; j < value.length; j++) {
          nvalue.array.data[j]=this.eval(value[j]);
        }
      }
      return nvalue;
    }
    return { value : value };
  }

  var Parser = function(value) {
    return this;
  }

  Parser.prototype.process = function(value) {
    return this.eval(value);
  }

  Parser.prototype.eval = function(value) {
    for (attr in value) {
      localAttr=attr.replace(/\./g, '_');
      if ( this[localAttr] != undefined ) {
        return this[localAttr](value[attr]);
      } else {
        return '[Unparsed] '+value[attr];
      }
    }
  }

  Parser.prototype.array = function(value) {
    var list = value.data.value;
    var result = new Array();

    if ( list.length == undefined ) {
      if ( list.value == undefined ) {
        result[0]=this.eval(list);
      } else {
        result[0]=this.eval(list.value);
      }
    } else {
      for (var i=0; i<list.length; i++) {
        if ( list[i].value != undefined ) {
          result[i]=this.eval(list[i].value);
        } else {
          result[i]=this.eval(list[i]);
        }
      }
    }
    return result;
  }

  Parser.prototype.struct = function(value) {
    var list = value.member;
    var result = new Object();

    if ( list.length == undefined ) {
      result[list.name]=this.eval(list.value);
    } else {
      for (var i=0; i<list.length; i++) {
        result[list[i].name]=this.eval(list[i].value);
      }
    }
    return result;
  }
  Parser.prototype.boolean = function(value) {
    return Boolean(value);
  }
  Parser.prototype.string = function(value) {
    return value;
  }
  Parser.prototype.number = function(value) {
    return parseInt(value);
  }
  Parser.prototype.dateTime_iso8601 = function(value) {
    var year   = parseInt(value.substr(0,4));
    var month  = parseInt(value.substr(4,2));
    var day    = parseInt(value.substr(6,2));
    var hour   = parseInt(value.substr(9,2));
    var minute = parseInt(value.substr(12,2));
    var second = parseInt(value.substr(15,2));
    return new Date(year, month, day, hour, minute, second);
  }
  Parser.prototype.int = function(value) {
    return parseInt(value);
  }

  var prep = new Prepare();

  var p=new Array();
  for (var i=0; i<parameters.length; i++) {
    p[i]=prep.eval(parameters[i]);
  }

  var xotree = new XML.ObjTree();
  var reqtree = {
      methodCall: {
          methodName: method,
          params: {
              param: p,
          }
      }
  };

  var reqxml = xotree.writeXML( reqtree );       // JS-Object to XML code
  var resxml = new JKL.ParseXML( url, reqxml );

  resxml.async(function(data) {
    var parser = new Parser();
    if ( data.methodResponse.fault != undefined ) {
      var fault=parser.eval(data.methodResponse.fault.value);
      failCallback(fault.faultString);
    } else {
      callback(parser.process(data.methodResponse.params.param.value));
    }
  });
  resxml.parse();
}
