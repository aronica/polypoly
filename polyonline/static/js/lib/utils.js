// Utils, private tools for web development
;(function(self, factory) {
  self.Utils = factory(self)
})(this, function(self) {
  'use strict';

  var Utils = {
    isDebug: true
  }
  // set debug mode to show the debugging log
  Utils.log = function() {
    if (Utils.isDebug && self.console) {
      self.console.log.apply(self.console, arguments)
    }
  }

  // 数组的交差并
  Utils.arrIntersection = function(arr1, arr2) {}
  Utils.arrSubstract = function(arr1, arr2) {}
  Utils.arrMerge = function(arr1, arr2) {}


  // format Date object to string
  Utils.formatDate = function(dt, format) {
    // Utils.log('[Utils] date format is: %s, date is: %s', format, dt)
    
    format = format || 'yMdhms'
    
    // get the last two letters of str
    function _lengthAlignment(str) {
      str = '0' + str
      var len = str.length
      return str.slice(len - 2, len)
    }
  
    var month = _lengthAlignment(dt.getMonth() + 1)
    var date = _lengthAlignment(dt.getDate())
    var hour = _lengthAlignment(dt.getHours())
    var minute = _lengthAlignment(dt.getMinutes())
    var second = _lengthAlignment(dt.getSeconds())
  
    return format.replace(/y/g, dt.getFullYear())
                 .replace(/M/g, month)
                 .replace(/d/g, date)
                 .replace(/h/g, hour)
                 .replace(/m/g, minute)
                 .replace(/s/g, second)
  }
  
  return Utils
})
