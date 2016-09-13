// the ajax methd based on fetch(https://github.com/camsong/fetch-ie8)
;(function(self, factory) {
  self.Ajax = factory(self)
})(this, function(self) {
  'use strict';

  function genRequestData(url, data) {
    // if data is null, return url
    if (!data) {
      return url
    }
    
    url += '?'
  
    for (var item in data) {
      url += item + '=' + data[item] + '&'
    }
  
    return url.replace(/&$/, '')
  }
  

  // Ajax, get and post method for ajax
  var Ajax = function() {}

  function createXMLHTTPRequest() {
    var xmlHttpRequest
    if (window.XMLHttpRequest) {
      xmlHttpRequest = new XMLHttpRequest()
      if (xmlHttpRequest.overrideMimeType) {
        xmlHttpRequest.overrideMimeType('text/xml')
      }
    } else if (window.ActiveXObject) {
      var activexName = ['MSXML2.XMLHTTP', 'Microsoft.XMLHTTP']
      for ( var i = 0; i < activexName.length; i++) {
        try {
          xmlHttpRequest = new ActiveXObject(activexName[i])
          if (xmlHttpRequest) break
        } catch (e) {
        }
      }
    }
    return xmlHttpRequest
  }     

  Ajax.prototype.get = function(url, data, callback, self) {
    url = genRequestData(url, data)
    Utils.log('[Ajax] generated url is: %s', url)
    if (typeof window.fetch === 'function') {
      fetch(url)
        .then(function(result) {
          return result.json()
        }).then(function(json) {
          if (json.res_code === 200) {
            Utils.log('[Ajax] fetch data is: %o', json.data)
            // callback for every request
            callback(json.data)
          } else {
            Utils.log('[Ajax] fetch error, res_code is: %s, res_msg is: %s', json.res_code, json.res_msg) 
            callback(null)
          }
        }).catch(function(error) {
          Utils.log('[Ajax] fetch failed:  %s', error)
        })
    } else {
        var req = createXMLHTTPRequest();
        if (req) {
          req.open('get', url, true);
          req.onreadystatechange = function() {
            if (req.readyState === 4) {
              if (req.status === 200) {
                var data = JSON.parse(req.response)
                console.log(data)
                callback(data.data)
              } else {
                callback(null)
              }
            }
          }
        req.send(null);
      }
    }
  }

  // TODO
  Ajax.prototype.post = function(url, data, callback, self) {}
  
  return Ajax
})
